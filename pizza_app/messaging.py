from django.utils import timezone
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase

from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter 
from reportlab.lib.units import cm

def generate_pdf(message_dict):
   order = message_dict['order']
   
   buffer = BytesIO()
   p = canvas.Canvas(buffer, pagesize=letter)
   p.setFont('Helvetica', 20)
   p.drawString(150, 700, f"Order#{order.pk}. Report generated at "+timezone.now().strftime('%Y-%b-%d'))
   p.setFont('Helvetica', 14)
   p.drawString(150, 650, f"Order placed by {order.customer.username}. Subtotal: {order.total_price} kr")
   p.setFont('Helvetica', 14)
   y = 650
   for final_line_item in order.final_line_items.all():
      y = y-50 
      p.drawString(220, y, f"- {final_line_item}")

   p.showPage()
   p.save()
   pdf = buffer.getvalue()
   buffer.close()
   return pdf

def admin_order_email(message_dict):
   contents = f"""
   You successfully placed order #{message_dict['order_id']} today. See more details about your order here: http://127.0.0.1:8000/thank_you/{message_dict['order_id']}
   """

   pdf = generate_pdf(message_dict)

   msg = EmailMessage(f"order #{message_dict['order_id']} placed", None, 'ambertheil96@gmail.com', ['joshkap2015@gmail.com', 'ambertheil96@gmail.com'])
   msg.attach('Your Order.pdf', pdf, 'application/pdf')
   msg.send()

def user_order_email(message_dict):
   contents = f"""
   You successfully placed order #{message_dict['order_id']} today. See more details about your order here: http://127.0.0.1:8000/thank_you/{message_dict['order_id']}
   """

   img_data = open('media/logo.jpg', 'rb').read()

   html_part = MIMEMultipart(_subtype='related')

   body = MIMEText(f"<p><img src='cid:logo' /> You successfully placed order #{message_dict['order_id']} today. See more details about your order here: http://127.0.0.1:8000/thank_you/{message_dict['order_id']}</p>", _subtype='html')
   html_part.attach(body)

   img = MIMEImage(img_data, 'jpeg')
   img.add_header('Content-Id', '<logo>')  # angle brackets are important
   img.add_header("Content-Disposition", "inline", filename="logo") # David Hess recommended this edit
   html_part.attach(img)

   msg = EmailMessage(f"order #{message_dict['order_id']} placed", None, 'ambertheil96@gmail.com', ['joshkap2015@gmail.com', 'ambertheil96@gmail.com'])
   msg.attach(html_part) # Attach the raw MIMEBase descendant. This is a public method on EmailMessage
   msg.send()




