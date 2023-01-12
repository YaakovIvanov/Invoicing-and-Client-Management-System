from PyPDF2 import PdfReader, PdfWriter
from PyPDF2.generic import NameObject, NumberObject


def gen_invoice(name=None,
    email=None,
    phone=None,
    invoice_date=None,
    invoice_num=None,
    services=None,
    description=None,
    item_price=None,
    item_quantity=None,
    item_total=None,
    deposit=None,
    paid_via=None,
    balance=None):

    data_dict = {"Name": name,
        "Email": email,
        "Phone": phone,
        "Invoice Date": invoice_date,
        "Invoice Number": invoice_num,
        "Services Selected": services,
        "Description of Work": description,
        "Item Price": item_price,
        "Item Quantity": item_quantity,
        "Item Total": item_total,
        "Deposit Paid": deposit,
        "Paid Via": paid_via,
        "Balance": balance,}

    reader = PdfReader("Form.pdf")
    writer = PdfWriter()

    page = reader.pages[0]

    # Copy form onto new pdf
    writer.add_page(page)

    # Fill out the form
    writer.update_page_form_field_values(
        writer.pages[0], data_dict
    )

    # Flatten the form
    for i in range(0, len(writer.pages[0]["/Annots"])):
        writer_annot = writer.pages[0]["/Annots"][i].getObject()
        for field in data_dict:
            if writer_annot.get("/T") == field:
                # make ReadOnly:
                writer_annot.update({NameObject("/Ff"): NumberObject(1)})

    # write "output" to PyPDF2-output.pdf
    with open(invoice_num + ".pdf", "wb") as output_stream:
        writer.write(output_stream)

def main():
    gen_invoice(name="Sample",
    phone="(012) 345 6789",
    email="sample@sample.com",
    invoice_date="00/00/9999",
    invoice_num="12345",
    services="Sample",
    description="Sample",
    item_price="$0",
    item_quantity="0",
    item_total="$0",
    deposit="$0",
    paid_via="PAID via Check",
    balance="$0",)


if __name__ == "__main__":
    main()
