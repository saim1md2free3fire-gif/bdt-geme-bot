import os
import google.generativeai as genai
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

# আপনার টেলিগ্রাম বট টোকেন এবং জেমিনি এপিআই কি
TELEGRAM_BOT_TOKEN = "8724046321:AAEw3SYzPIGE2MMWZeWPFIAozfllfLmQt6E
GEMINI_API_KEY = "AQ.Ab8RN6KK6E2Nl70mtyFMfb9RaU3s5DbgWDOVcIm_nRoV6DTTlA"

# জেমিনি কনফিগারেশন
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')

# সিস্টেম প্রম্পট বা গেম এনালাইসিস লজিক
SYSTEM_INSTRUCTION = """
তুমি একজন প্রফেশনাল গেম সিগন্যাল অ্যানালিস্ট। ব্যবহারকারী যখন গেমের হিস্ট্রি বা চার্টের স্ক্রিনশট পাঠাবে,
তখন তুমি পিরিয়ড, নাম্বার এবং বিগ/স্মল (Big/Small) ট্রেন্ড গভীরভাবে বিশ্লেষণ করবে।
ক্লাস্টার রুল, পিং-পং (1-to-1) রুল এবং ট্রেন্ড রিভার্সাল বা ফেকআউট লজিক মাথায় রেখে পরবর্তী রাউন্ডের জন্য সম্ভাব্য সিগন্যাল (যেমন: Big অথবা Small) প্রদান করবে।
"""

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo_file = await update.message.photo[-1].get_file()
    
    # ছবি ডাউনলোড করা
    photo_path = "temp_game_screenshot.jpg"
    await photo_file.download_to_drive(photo_path)
    
    await update.message.reply_text("🔍 স্ক্রিনশট বিশ্লেষণ করা হচ্ছে, দয়া করে অপেক্ষা করুন...")
    
    try:
        # জেমিনি ভিশন এপিআই-এর মাধ্যমে ছবি আপলোড ও প্রসেস করা
        sample_file = genai.upload_file(path=photo_path, mime_type="image/jpeg")
        
        prompt = f"{SYSTEM_INSTRUCTION}\n\nএই গেমের স্ক্রিনশটটি দেখে পরবর্তী পিরিয়ডের জন্য সঠিক সিগন্যাল ও বিশ্লেষণ প্রদান করো।"
        response = model.generate_content([sample_file, prompt])
        
        # ইউজারের কাছে উত্তর পাঠানো
        await update.message.reply_text(response.text)
        
    except Exception as e:
        await update.message.reply_text(f"দুঃখিত, এনালাইসিস করতে সমস্যা হয়েছে: {str(e)}")
        
    # টেম্পোরারি ফাইল রিমুভ করা
    if os.path.exists(photo_path):
        os.remove(photo_path)

if __name__ == '__main__':
    # টেলিগ্রাম বট অ্যাপ ইনিশিয়ালাইজ করা
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    
    # ছবি হ্যান্ডলার যোগ করা
    application.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    
    print("বট সফলভাবে চালু হয়েছে এবং কাজ করছে...")
    application.run_polling()
