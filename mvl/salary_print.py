import os,json

from PyPDF2 import PdfWriter

import frappe
from frappe import _
from frappe.core.doctype.access_log.access_log import make_access_log
from frappe.utils import now_datetime, formatdate,random_string
from frappe.translate import print_language
from frappe.utils.pdf import get_pdf
from frappe.utils.background_jobs import enqueue


no_cache = 1

base_template_path = "www/printview.html"
standard_format = "templates/print_formats/standard.html"

from frappe.www.printview import validate_print_permission

@frappe.whitelist()
def enqueue_download_multi_pdf(start_date,end_date,arrear_slip,unit=None,department=None):
    conditions = ''
    if unit:
        conditions += 'and unit="%s"' % unit
    if department:
        conditions += 'and department="%s"' % department
    if arrear_slip:
        salary_slips = frappe.db.sql("Select name from `tabSalary Slip` where start_date = '%s' and end_date = '%s' and arrear_slip = '%s' %s" % (start_date,end_date,arrear_slip,conditions),as_list=1,pluck="name")
    else:
        salary_slips = frappe.db.sql("Select name from `tabSalary Slip` where start_date = '%s' and end_date = '%s' %s" % (start_date,end_date,conditions),as_list=1,pluck="name")
    enqueue(download_multi_pdf, queue='default', timeout=6000, event='download_multi_pdf',doctype="Salary Slip", name=json.dumps(salary_slips), format='Pay Slip')
    frappe.msgprint("Bulk Salary Slip Download is successsfully Initiated. Kindly wait for sometime and refresh the page.")

    
@frappe.whitelist()
def download_multi_pdf(
    doctype, name, format=None, no_letterhead=False, letterhead=None, options=None
):
    """
    Concatenate multiple docs as PDF .

    Returns a PDF compiled by concatenating multiple documents. The documents
    can be from a single DocType or multiple DocTypes

    Note: The design may seem a little weird, but it exists exists to
            ensure backward compatibility. The correct way to use this function is to
            pass a dict to doctype as described below

    NEW FUNCTIONALITY
    =================
    Parameters:
    doctype (dict):
            key (string): DocType name
            value (list): of strings of doc names which need to be concatenated and printed
    name (string):
            name of the pdf which is generated
    format:
            Print Format to be used

    Returns:
    PDF: A PDF generated by the concatenation of the mentioned input docs

    OLD FUNCTIONALITY - soon to be deprecated
    =========================================
    Parameters:
    doctype (string):
            name of the DocType to which the docs belong which need to be printed
    name (string or list):
            If string the name of the doc which needs to be printed
            If list the list of strings of doc names which needs to be printed
    format:
            Print Format to be used

    Returns:
    PDF: A PDF generated by the concatenation of the mentioned input docs
    """

    import json

    output = PdfWriter()

    if isinstance(options, str):
        options = json.loads(options)

    if not isinstance(doctype, dict):
        result = json.loads(name)

        # Concatenating pdf files
        for i, ss in enumerate(result):
            output = frappe.get_print(
                doctype,
                ss,
                format,
                as_pdf=True,
                output=output,
                no_letterhead=no_letterhead,
                letterhead=letterhead,
                pdf_options=options,
            )
        filename = "{doctype}.pdf".format(
            doctype=doctype.replace(" ", "-").replace("/", "-")
        )
    else:
        for doctype_name in doctype:
            for doc_name in doctype[doctype_name]:
                try:
                    output = frappe.get_print(
                        doctype_name,
                        doc_name,
                        format,
                        as_pdf=True,
                        output=output,
                        no_letterhead=no_letterhead,
                        letterhead=letterhead,
                        pdf_options=options,
                    )
                except Exception:
                    frappe.log_error(
                        title="Error in Multi PDF download",
                        message=f"Permission Error on doc {doc_name} of doctype {doctype_name}",
                        reference_doctype=doctype_name,
                        reference_name=doc_name,
                    )
        filename = f"{name}.pdf"
    ret = frappe.get_doc({
            "doctype": "File",
            "attached_to_name": 'Reports Dashboard',
            "attached_to_doctype": 'Reports Dashboard',
            "attached_to_field": 'salary_slips',
            "file_name": filename,
            "is_private": 0,
            "content": read_multi_pdf(output),
            "decode": False
        })
    ret.save(ignore_permissions=True)
    frappe.db.commit()
    attached_file = frappe.get_doc("File", ret.name)
    frappe.db.set_value('Reports Dashboard',None,'salary_slips',attached_file.file_url)
    frappe.db.set_value('Reports Dashboard',None,'last_download_on',now_datetime())


def read_multi_pdf(output):
    frappe.log_error(title='type',message=type(output))
    # Get the content of the merged pdf files
    fname = os.path.join("/tmp", f"frappe-pdf-{frappe.generate_hash()}.pdf")
    output.write(open(fname, "wb"))

    with open(fname, "rb") as fileobj:
        filedata = fileobj.read()

    return filedata