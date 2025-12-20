
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order


@receiver(post_save, sender=Order)
def order_notification(sender, instance, created, **kwargs):

    if created:
        # Order was just created
        print(f"\n{'='*60}")
        print(f"ORDER CREATED NOTIFICATION")
        print(f"{'='*60}")
        print(f"Order ID: #{instance.id}")
        print(f"Customer: {instance.user.email}")
        print(f"Total Amount: ${instance.total_amount}")
        print(f"Status: {instance.status}")
        print(f"Items: {instance.items.count()}")
        print(f"{'='*60}\n")
        
        # In production, you would send actual email:
        # send_mail(
        #     subject=f'Order #{instance.id} Confirmed',
        #     message=f'Your order has been placed successfully...',
        #     from_email='noreply@ecommerce.com',
        #     recipient_list=[instance.user.email],
        # )
    
    elif instance.status == 'cancelled':
        # Order was cancelled
        print(f"\n{'='*60}")
        print(f"ORDER CANCELLED NOTIFICATION")
        print(f"{'='*60}")
        print(f"Order ID: #{instance.id}")
        print(f"Customer: {instance.user.email}")
        print(f"Status: {instance.status}")
        print(f"Stock has been restored")
        print(f"{'='*60}\n")