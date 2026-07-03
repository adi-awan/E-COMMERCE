from io import BytesIO
from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
)
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet


def generate_invoice(order):

    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer)

    styles = getSampleStyleSheet()

    elements = []

    elements.append(
        Paragraph(
            "<b>INVOICE</b>",
            styles["Title"]
        )
    )

    elements.append(
        Paragraph(
            f"Order ID: {order['order']['id']}",
            styles["Normal"]
        )
    )

    elements.append(
        Paragraph(
            f"Customer: {order['shipping']['full_name']}",
            styles["Normal"]
        )
    )

    elements.append(
        Paragraph(
            f"Email: {order['shipping']['email']}",
            styles["Normal"]
        )
    )

    elements.append(
        Paragraph(
            f"Status: {order['order']['status']}",
            styles["Normal"]
        )
    )

    data = [
        [
            "Product",
            "Qty",
            "Price"
        ]
    ]

    for item in order["items"]:

        data.append([
            item["products"]["name"],
            str(item["quantity"]),
            f"Rs. {item['price']}"
        ])

    data.append([
        "",
        "Total",
        f"Rs. {order['order']['total_amount']}"
    ])

    table = Table(data)

    table.setStyle(

        TableStyle([

            (
                "BACKGROUND",
                (0,0),
                (-1,0),
                colors.grey
            ),

            (
                "TEXTCOLOR",
                (0,0),
                (-1,0),
                colors.white
            ),

            (
                "GRID",
                (0,0),
                (-1,-1),
                1,
                colors.black
            ),

            (
                "BACKGROUND",
                (0,1),
                (-1,-1),
                colors.beige
            )

        ])

    )

    elements.append(table)

    doc.build(elements)

    buffer.seek(0)

    return buffer