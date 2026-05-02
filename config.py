# config.py
DEBUG_PAYMENTS = os.getenv("DEBUG_PAYMENTS", "False").lower() == "true"

# handlers/payment.py
@router.callback_query(F.data == "boost_listing")
async def boost_listing(callback: CallbackQuery):
    if DEBUG_PAYMENTS:
        # Simulate successful payment
        await on_successful_payment(callback.message)
        return
    # else: real invoice flow