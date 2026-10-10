import os
import google.generativeai as genai
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

# আপনার টেলিগ্রাম বট টোকেন এবং জেমিনি এপিআই কি
TELEGRAM_BOT_TOKEN = "8724046321:AAGZPt8-AxUzIoNbDR75VE91-azZLAERdOk"
GEMINI_API_KEY = "AQ.AbIRn6KK6E2nl70mtyFMfb9RzU3s50bgMD0Vcin_nRoV6DTT1A"

# জেমিনি কনফিগারেশন
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')

# সিস্টেম প্রম্পট বা গেম অ্যানালাইসিস লজিক
SYSTEM_INSTRUCTION = """
তুমি একজন প্রফেশনাল গেম সিগন্যাল অ্যানালিস্ট। ব্যবহারকারী যখন গেমের উইঙ্গো বা কালার প্রেডিকশন স্ক্রিনশট পাঠাবে,
তখন তুমি বিশ্লেষণ করে পরবর্তী রাউন্ডের সম্ভাব্য সিগন্যাল (যেমন: Big অথবা Small) এবং কালার প্রেডিকশন দিবে।
"""

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo_file = await update.message.photo[-1].get_file()
    
    # ছবি ডাউনলোড করা
    photo_path = "temp_game_screenshot.jpg"
    await photo_file.download_to_drive(photo_path)
    
    await update.message.reply_text("🔍 স্ক্রিনশট বিশ্লেষণ করা হচ্ছে, অনুগ্রহ করে অপেক্ষা করুন...")
    
    try:
        # জেমিনি দিয়ে ছবি আপলোড ও প্রসেস করা
        sample_file = genai.upload_file(path=photo_path, mime_type="image/jpeg")
        
        prompt = f"{SYSTEM_INSTRUCTION}\n\nএই গেমের স্ক্রিনশট দেখে পরবর্তী রাউন্ডের জন্য সঠিক সিগন্যাল ও বিশ্লেষণ প্রদান করো।"
        response = model.generate_content([sample_file, prompt])
        
        # ইউজারকে উত্তর পাঠানো
        await update.message.reply_text(response.text)
        
    except Exception as e:
        await update.message.reply_text(f"দুঃখিত, অ্যানালাইসিস করতে সমস্যা হয়েছে: {str(e)}")
        
    # সাময়িক ফাইল মুছে ফেলা
    if os.path.exists(photo_path):
        os.remove(photo_path)

if __name__ == '__main__':
    # টেলিগ্রাম বট অ্যাপ ইনিশিয়ালাইজ করা
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    
    # ছবি হ্যান্ডলার যোগ করা
    application.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    
    print("বট সফলভাবে চালু হয়েছে এবং কাজ করছে...")
    application.run_polling()
