from django.core.mail import send_mail

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
   Joshua Kaplan placed order #{message_dict['order_id']} today. See more details about the order here: http://127.0.0.1:8000/thank_you/{message_dict['order_id']}
   """
   send_mail(
      f"Pizza Express Order #{message_dict['order_id']}",
      contents,
      'joshua@ptd-cph.com',
      ['joshkap2015@gmail.com', 'ambertheil96@gmail.com'],
      fail_silently=False,
   )
   print(f"Admin order email sent for order #{message_dict['order_id']}")

def user_order_email(message_dict):
   contents = f"""
   You successfully placed order #{message_dict['order_id']} today. See more details about your order here: http://127.0.0.1:8000/thank_you/{message_dict['order_id']}
   """
   send_mail(
      f"Pizza Express Order #{message_dict['order_id']}",
      contents,
      'joshua@ptd-cph.com',
      ['joshkap2015@gmail.com', 'ambertheil96@gmail.com'],
      fail_silently=False,
   )
   print(f"User order email sent for order #{message_dict['order_id']}")