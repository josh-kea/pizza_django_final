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

def email_message(message_dict):
   contents = f"""
   Hi, thank you for trying to reset your password.
   Your token is: {message_dict['token']}
   """
   send_mail(
      'Password Reset Token',
      contents,
      'joshkap2015@gmail.com',
      [message_dict['email']],
      fail_silently=False
   )

def admin_order_email(message_dict):
   contents = f"""
   You successfully placed order #{message_dict['order_id']} today. See more details about your order here: http://127.0.0.1:8000/thank_you/{message_dict['order_id']}
   """

   print(message_dict['order'].pk)

   pdf = generate_pdf(message_dict)

   msg = EmailMessage(f"order #{message_dict['order_id']} placed", None, 'ambertheil96@gmail.com', ['joshkap2015@gmail.com', 'ambertheil96@gmail.com'])
   msg.attach('Your Order.pdf', pdf, 'application/pdf')
   msg.send()
   print(f"Admin order email sent for order #{message_dict['order_id']}")

def user_order_email(message_dict):
   contents = f"""
   You successfully placed order #{message_dict['order_id']} today. See more details about your order here: http://127.0.0.1:8000/thank_you/{message_dict['order_id']}
   """
      # Load the image you want to send as bytes
   img_data = open('media/logo.jpg', 'rb').read()

   # Create a "related" message container that will hold the HTML 
   # message and the image. These are "related" (not "alternative")
   # because they are different, unique parts of the HTML message,
   # not alternative (html vs. plain text) views of the same content.
   html_part = MIMEMultipart(_subtype='related')

   # Create the body with HTML. Note that the image, since it is inline, is 
   # referenced with the URL cid:myimage... you should take care to make
   # "myimage" unique
   body = MIMEText(f"<p><img src='cid:logo' /> You successfully placed order #{message_dict['order_id']} today. See more details about your order here: http://127.0.0.1:8000/thank_you/{message_dict['order_id']}</p>", _subtype='html')
   html_part.attach(body)


   # Now create the MIME container for the image
   img = MIMEImage(img_data, 'jpeg')
   img.add_header('Content-Id', '<logo>')  # angle brackets are important
   img.add_header("Content-Disposition", "inline", filename="logo") # David Hess recommended this edit
   html_part.attach(img)

   # Configure and send an EmailMessage
   # Note we are passing None for the body (the 2nd parameter). You could pass plain text
   # to create an alternative part for this message
   msg = EmailMessage(f"order #{message_dict['order_id']} placed", None, 'ambertheil96@gmail.com', ['joshkap2015@gmail.com', 'ambertheil96@gmail.com'])
   msg.attach(html_part) # Attach the raw MIMEBase descendant. This is a public method on EmailMessage
   msg.send()


   print(f"User order email sent for order #{message_dict['order_id']}")




