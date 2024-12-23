
# TofahaBot: نظام ذكي لمراقبة وتحليل التفاح (واجهة برمجة التطبيقات ولوحة القيادة فقط)

**TofahaBot** هو جزء من نظام شامل لتحليل حالة فاكهة التفاح في المزارع باستخدام تقنيات الذكاء الاصطناعي والرؤية الحاسوبية. يحتوي هذا المستودع فقط على **واجهة برمجة التطبيقات (API)** ولوحة التحكم (Dashboard) الخاصة بالنظام، بينما الجزء الآخر يعمل مباشرة على الروبوت (آلة ذاتية القيادة) الذي يقوم بالعمليات داخل المزرعة.

---

## الأجزاء الرئيسية للمشروع

### 1. هذا الجزء: واجهة برمجة التطبيقات ولوحة التحكم
#### واجهة برمجة التطبيقات (API):
- استقبال البيانات التي يجمعها الروبوت، مثل:
  - عدد التفاح المكتشف.
  - حالة التفاح (سليم/تالف).
  - صور التفاح التالف.
  - بيانات حركة الروبوت مثل الاتجاهات والإشارات المكتشفة.
- تخزين البيانات في قاعدة بيانات "مونجو دي بي".

#### لوحة التحكم:
- عرض الإحصائيات مثل عدد التفاح المكتشف وتصنيف حالته.
- عرض الصور المرتبطة بالتفاح التالف.
- تقديم واجهة سهلة للمزارعين لمراقبة وتحليل البيانات في الوقت الحقيقي.

---

### 2. الجزء الآخر (غير مدرج هنا): الروبوت العامل في المزرعة
#### مكان تشغيله:
- يعمل مباشرة على الروبوت (آلة ذاتية القيادة) المزودة براسبيري باي.

#### مهامه:
- التنقل بين الأشجار باستخدام إشارات المرور التي تقوده (يمين، يسار، قف، دوران).
- تشغيل نموذج YOLO لاكتشاف وتحليل التفاح.
- التعرف على التفاح التالف وإزالته باستخدام ذراع ميكانيكية.
- إرسال البيانات والصور التي يجمعها إلى واجهة برمجة التطبيقات.

---

## المزايا
1. تكامل البيانات بين الروبوت وواجهة برمجة التطبيقات.
2. لوحة تحكم ديناميكية لعرض المعلومات بشكل فوري.
3. تحسين جودة المحاصيل وتقليل الهدر باستخدام الذكاء الاصطناعي.

---

## كيفية الاستخدام

### المتطلبات
- بايثون 3.8+
- مكتبات:
  - Flask
  - Dash
  - pymongo
  - pandas
- قاعدة بيانات "مونجو" مثبتة ومفعلة.
- مجلد `static/images/` لحفظ الصور.

### خطوات التشغيل
1. قم بتثبيت المتطلبات:
2. شغل قاعدة بيانات.
3. شغل واجهة برمجة التطبيقات:
   ```bash
   python app.py
   ```
4. افتح المتصفح وانتقل إلى:
   - لوحة التحكم: `http://localhost:5000/dashboard/`
   - API: نقاط النهاية مثل `/api/robot/apples`.

---

## ملاحظات
- هذا المستودع مخصص فقط لواجهة برمجة التطبيقات ولوحة القيادة.
- الجزء الخاص بتحكم الروبوت ومعالجة البيانات المحلية يعمل على الروبوت نفسه في المزرعة.

---

## المساهمة
مرحب بأي مساهمة لتطوير هذا النظام. يرجى إرسال طلبات السحب (Pull Requests) أو فتح قضايا (Issues) على صفحة المستودع.

---

## الرخصة
هذا المشروع مفتوح المصدر تحت رخصة MIT.
