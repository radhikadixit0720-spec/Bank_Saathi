// Static UI copy in English, Hindi, and Hinglish. Dynamic content (form
// field labels, checklist items, validation messages, disclaimers) is
// translated server-side instead - the frontend just forwards the current
// `lang` to the API (see api/client.js) and renders whatever comes back.

export const TRANSLATIONS = {
  // --- Brand / nav ---
  brand_name: { en: 'Bank Saathi', hi: 'बैंक साथी', hinglish: 'Bank Saathi' },
  brand_tagline: { en: 'Your smart banking companion', hi: 'आपका स्मार्ट बैंकिंग साथी', hinglish: 'Aapka smart banking saathi' },
  nav_customer_section: { en: 'Customer', hi: 'ग्राहक', hinglish: 'Customer' },
  nav_staff_section: { en: 'Bank Staff', hi: 'बैंक स्टाफ़', hinglish: 'Bank staff' },
  nav_dashboard: { en: 'Dashboard', hi: 'डैशबोर्ड', hinglish: 'Dashboard' },
  nav_form_scanner: { en: 'Form Scanner', hi: 'फ़ॉर्म स्कैनर', hinglish: 'Form Scanner' },
  nav_language_assistant: { en: 'Simple Language', hi: 'सरल भाषा सहायक', hinglish: 'Simple Language' },
  nav_checklist: { en: 'Document Checklist', hi: 'दस्तावेज़ चेकलिस्ट', hinglish: 'Document Checklist' },
  nav_error_checker: { en: 'Error Checker', hi: 'त्रुटि जाँचकर्ता', hinglish: 'Error Checker' },
  nav_status_vault: { en: 'Status & Receipts', hi: 'स्थिति और रसीदें', hinglish: 'Status & Receipts' },
  nav_appointment: { en: 'Branch Token', hi: 'शाखा टोकन', hinglish: 'Branch Token' },
  nav_employee: { en: 'Employee Dashboard', hi: 'कर्मचारी डैशबोर्ड', hinglish: 'Employee Dashboard' },
  nav_footer: {
    en: 'Prototype product. Final verification always happens with bank staff.',
    hi: 'यह एक प्रोटोटाइप उत्पाद है। अंतिम सत्यापन हमेशा बैंक स्टाफ़ द्वारा होता है।',
    hinglish: 'Yeh ek prototype product hai. Final verification hamesha bank staff ke through hoti hai.',
  },
  nav_classic_walkthrough: {
    en: 'Open original guided walkthrough →',
    hi: 'मूल गाइडेड वॉकथ्रू खोलें →',
    hinglish: 'Original guided walkthrough kholein →',
  },
  your_name_placeholder: { en: 'Your name', hi: 'आपका नाम', hinglish: 'Aapka naam' },

  // --- Page titles/subtitles (keyed by route) ---
  title_home: { en: 'Welcome back', hi: 'वापसी पर स्वागत है', hinglish: 'Wapas swagat hai' },
  subtitle_home: {
    en: 'Everything you need for your banking visit, in one place',
    hi: 'आपकी बैंकिंग विज़िट के लिए सब कुछ, एक ही जगह पर',
    hinglish: 'Aapki banking visit ke liye sab kuch, ek hi jagah par',
  },
  title_form_scanner: { en: 'Form Scanner', hi: 'फ़ॉर्म स्कैनर', hinglish: 'Form Scanner' },
  subtitle_form_scanner: {
    en: 'Upload a form and check it against a bank template',
    hi: 'एक फ़ॉर्म अपलोड करें और उसे बैंक टेम्पलेट से जाँचें',
    hinglish: 'Ek form upload karein aur usse bank template se check karein',
  },
  title_language_assistant: { en: 'Simple Language Assistant', hi: 'सरल भाषा सहायक', hinglish: 'Simple Language Assistant' },
  subtitle_language_assistant: {
    en: 'Turn formal banking text into plain language',
    hi: 'औपचारिक बैंकिंग टेक्स्ट को सरल भाषा में बदलें',
    hinglish: 'Formal banking text ko simple bhasha mein badlein',
  },
  title_checklist: { en: 'Document Checklist', hi: 'दस्तावेज़ चेकलिस्ट', hinglish: 'Document Checklist' },
  subtitle_checklist: {
    en: 'Know exactly what to carry before you visit',
    hi: 'विज़िट से पहले जानें कि क्या साथ ले जाना है',
    hinglish: 'Visit se pehle jaanein kya saath le jaana hai',
  },
  title_error_checker: { en: 'Error Checker', hi: 'त्रुटि जाँचकर्ता', hinglish: 'Error Checker' },
  subtitle_error_checker: {
    en: 'Catch mistakes before you submit',
    hi: 'सबमिट करने से पहले गलतियाँ पकड़ें',
    hinglish: 'Submit karne se pehle galtiyaan pakdein',
  },
  title_status_vault: { en: 'Status & Receipt Vault', hi: 'स्थिति और डिजिटल रसीद वॉल्ट', hinglish: 'Status & Receipt Vault' },
  subtitle_status_vault: {
    en: 'Track your requests and digital receipts',
    hi: 'अपने अनुरोधों और डिजिटल रसीदों को ट्रैक करें',
    hinglish: 'Apne requests aur digital receipts track karein',
  },
  title_appointment: { en: 'Branch Token', hi: 'शाखा टोकन', hinglish: 'Branch Token' },
  subtitle_appointment: {
    en: 'Prototype digital queue - skip the line',
    hi: 'प्रोटोटाइप डिजिटल क्यू - लाइन छोड़ें',
    hinglish: 'Prototype digital queue - line skip karein',
  },
  title_employee: { en: 'Employee Dashboard', hi: 'कर्मचारी डैशबोर्ड', hinglish: 'Employee Dashboard' },
  subtitle_employee: {
    en: 'Customer requests, missing documents and alerts',
    hi: 'ग्राहक अनुरोध, छूटे हुए दस्तावेज़ और अलर्ट',
    hinglish: 'Customer requests, missing documents aur alerts',
  },

  // --- Dashboard ---
  hero_greeting: { en: 'Namaste', hi: 'नमस्ते', hinglish: 'Namaste' },
  hero_desc: {
    en: 'Bank Saathi helps you understand forms, know what documents to carry, catch mistakes before you submit, and track every request - so you visit the branch fewer times.',
    hi: 'Bank Saathi आपको फ़ॉर्म समझने, दस्तावेज़ जानने, गलतियाँ पकड़ने और हर अनुरोध को ट्रैक करने में मदद करता है - ताकि आपको शाखा कम बार जाना पड़े।',
    hinglish: 'Bank Saathi aapko forms samajhne, documents jaanne, galtiyaan pakadne aur har request track karne mein madad karta hai - taaki aapko branch kam baar jaana pade.',
  },
  pending_requests: { en: 'Pending Requests', hi: 'लंबित अनुरोध', hinglish: 'Pending Requests' },
  completed_requests: { en: 'Completed Requests', hi: 'पूर्ण अनुरोध', hinglish: 'Completed Requests' },
  total_requests: { en: 'Total Requests', hi: 'कुल अनुरोध', hinglish: 'Total Requests' },
  upcoming_token: { en: 'Upcoming Token', hi: 'आगामी टोकन', hinglish: 'Upcoming Token' },
  quick_actions: { en: 'Quick actions', hi: 'त्वरित कार्रवाई', hinglish: 'Quick actions' },
  recent_requests: { en: 'Recent requests', hi: 'हाल के अनुरोध', hinglish: 'Recent requests' },
  qa_form_scanner_desc: { en: 'Scan a form & match it to a template', hi: 'फ़ॉर्म स्कैन करें और टेम्पलेट से मिलाएँ', hinglish: 'Form scan karein aur template se match karein' },
  qa_language_desc: { en: 'Understand formal banking text', hi: 'औपचारिक बैंकिंग टेक्स्ट समझें', hinglish: 'Formal banking text samjhein' },
  qa_checklist_desc: { en: 'See what to carry for your visit', hi: 'विज़िट के लिए क्या ले जाना है देखें', hinglish: 'Visit ke liye kya le jaana hai dekhein' },
  qa_error_desc: { en: 'Catch mistakes before submitting', hi: 'सबमिट करने से पहले गलतियाँ पकड़ें', hinglish: 'Submit se pehle galtiyaan pakdein' },
  qa_status_desc: { en: 'Track requests & receipts', hi: 'अनुरोध और रसीदें ट्रैक करें', hinglish: 'Requests aur receipts track karein' },
  qa_token_desc: { en: 'Get a prototype queue token', hi: 'प्रोटोटाइप क्यू टोकन पाएँ', hinglish: 'Prototype queue token lein' },

  // --- Form scanner ---
  fs_step1: { en: '1. Choose a form type', hi: '1. फ़ॉर्म प्रकार चुनें', hinglish: '1. Form type chunein' },
  fs_template_label: { en: 'Bank form template', hi: 'बैंक फ़ॉर्म टेम्पलेट', hinglish: 'Bank form template' },
  fs_step2: { en: '2. Upload your filled form', hi: '2. अपना भरा हुआ फ़ॉर्म अपलोड करें', hinglish: '2. Apna bhara hua form upload karein' },
  fs_upload_hint: { en: 'Click to upload a PDF or text file', hi: 'PDF या टेक्स्ट फ़ाइल अपलोड करने के लिए क्लिक करें', hinglish: 'PDF ya text file upload karne ke liye click karein' },
  fs_scan_btn: { en: 'Scan Form', hi: 'फ़ॉर्म स्कैन करें', hinglish: 'Form Scan Karein' },
  fs_scanning: { en: 'Scanning...', hi: 'स्कैन हो रहा है...', hinglish: 'Scan ho raha hai...' },
  fs_disclaimer: {
    en: 'Text-based PDFs are read for real and matched against the template. Images/scans without a text layer are honestly reported as "OCR not configured" rather than faking a result - see fallback notes below after scanning.',
    hi: 'टेक्स्ट-आधारित PDF वास्तव में पढ़े जाते हैं और टेम्पलेट से मिलाए जाते हैं। बिना टेक्स्ट लेयर वाली इमेज/स्कैन को ईमानदारी से "OCR कॉन्फ़िगर नहीं है" बताया जाता है, नकली परिणाम नहीं दिया जाता।',
    hinglish: 'Text-based PDFs sach mein padhe jaate hain aur template se match kiye jaate hain. Bina text layer wali images/scans ko honestly "OCR configured nahi hai" bataya jaata hai, fake result nahi diya jaata.',
  },
  fs_result_title: { en: 'Scan result', hi: 'स्कैन परिणाम', hinglish: 'Scan result' },
  fs_result_empty: { en: 'Upload a form to see field-by-field results here.', hi: 'फ़ील्ड-वार परिणाम देखने के लिए फ़ॉर्म अपलोड करें।', hinglish: 'Field-by-field results dekhne ke liye form upload karein.' },
  fs_matched: { en: 'matched', hi: 'मिला', hinglish: 'matched' },
  fs_missing: { en: 'missing', hi: 'छूटा', hinglish: 'missing' },
  fs_needs_attention: { en: 'needs attention', hi: 'ध्यान चाहिए', hinglish: 'needs attention' },
  fs_analyzing: { en: 'Analyzing your document...', hi: 'आपका दस्तावेज़ जाँचा जा रहा है...', hinglish: 'Aapka document check ho raha hai...' },

  // --- Language assistant ---
  la_paste_label: { en: 'Paste formal banking text', hi: 'औपचारिक बैंकिंग टेक्स्ट पेस्ट करें', hinglish: 'Formal banking text paste karein' },
  la_placeholder: { en: 'e.g. Please furnish proof of residential address.', hi: 'जैसे: कृपया निवास पते का प्रमाण प्रस्तुत करें।', hinglish: 'Jaise: Please furnish proof of residential address.' },
  la_submit_btn: { en: 'Get Simple Explanation', hi: 'सरल व्याख्या पाएँ', hinglish: 'Simple Explanation Paayein' },
  la_simplifying: { en: 'Simplifying...', hi: 'सरल बनाया जा रहा है...', hinglish: 'Simplify ho raha hai...' },
  la_try_example: { en: 'Try an example', hi: 'एक उदाहरण आज़माएँ', hinglish: 'Ek example try karein' },
  la_result_title: { en: 'Simple explanation', hi: 'सरल व्याख्या', hinglish: 'Simple explanation' },
  la_result_empty: { en: 'Your simple explanation will appear here.', hi: 'आपकी सरल व्याख्या यहाँ दिखाई देगी।', hinglish: 'Aapki simple explanation yahaan dikhegi.' },
  la_working: { en: 'Working out a simple explanation...', hi: 'सरल व्याख्या तैयार की जा रही है...', hinglish: 'Simple explanation taiyaar ho rahi hai...' },
  la_ai_generated: { en: 'AI-generated', hi: 'AI-जनित', hinglish: 'AI-generated' },
  la_rule_based: { en: 'Rule-based (no AI key configured)', hi: 'नियम-आधारित (कोई AI कुंजी कॉन्फ़िगर नहीं)', hinglish: 'Rule-based (koi AI key configure nahi hai)' },

  // --- Checklist ---
  cl_select_service: { en: 'Select a banking service', hi: 'एक बैंकिंग सेवा चुनें', hinglish: 'Ek banking service chunein' },
  cl_loading: { en: 'Loading checklist...', hi: 'चेकलिस्ट लोड हो रही है...', hinglish: 'Checklist load ho rahi hai...' },
  cl_tap_to_mark: { en: 'Tap to mark as', hi: 'चिह्नित करने के लिए टैप करें:', hinglish: 'Mark karne ke liye tap karein:' },

  // --- Error checker ---
  ec_enter_values: { en: 'Enter your form values', hi: 'अपने फ़ॉर्म मान दर्ज करें', hinglish: 'Apni form values daalein' },
  ec_consent: { en: 'I have read and accept the declaration', hi: 'मैंने घोषणा पढ़ ली है और स्वीकार करता/करती हूँ', hinglish: 'Maine declaration padh liya hai aur accept karta/karti hoon' },
  ec_signature: { en: 'I have signed the physical form', hi: 'मैंने भौतिक फ़ॉर्म पर हस्ताक्षर कर दिए हैं', hinglish: 'Maine physical form par sign kar diya hai' },
  ec_check_btn: { en: 'Check Errors', hi: 'त्रुटियाँ जाँचें', hinglish: 'Errors Check Karein' },
  ec_checking: { en: 'Checking...', hi: 'जाँच हो रही है...', hinglish: 'Check ho raha hai...' },
  ec_results_title: { en: 'Results', hi: 'परिणाम', hinglish: 'Results' },
  ec_results_empty: { en: 'Fill the form and click "Check Errors" to see results here.', hi: '\u0928\u0924\u0940\u091c\u0947 \u0926\u0947\u0916\u0928\u0947 \u0915\u0947 \u0932\u093f\u090f \u092b\u0949\u0930\u094d\u092e \u092d\u0930\u0947\u0902 \u0914\u0930 "\u0924\u094d\u0930\u0941\u091f\u093f\u092f\u093e\u0902 \u091c\u093e\u0902\u091a\u0947\u0902" \u092a\u0930 \u0915\u094d\u0932\u093f\u0915 \u0915\u0930\u0947\u0902।', hinglish: 'Form bharein aur "Errors Check Karein" par click karein results dekhne ke liye.' },
  ec_no_errors: { en: 'No errors found', hi: 'कोई त्रुटि नहीं मिली', hinglish: 'Koi error nahi mila' },
  field_account_number: { en: 'Account Number', hi: 'खाता संख्या', hinglish: 'Account Number' },
  field_mobile_number: { en: 'Mobile Number', hi: 'मोबाइल नंबर', hinglish: 'Mobile Number' },
  field_email: { en: 'Email Address', hi: 'ईमेल पता', hinglish: 'Email Address' },
  field_pan_number: { en: 'PAN Number', hi: 'पैन नंबर', hinglish: 'PAN Number' },
  field_dob: { en: 'Date of Birth (DD-MM-YYYY)', hi: 'जन्म तिथि (DD-MM-YYYY)', hinglish: 'Date of Birth (DD-MM-YYYY)' },

  // --- Status vault ---
  sv_submit_new: { en: 'Submit a new request', hi: 'नया अनुरोध सबमिट करें', hinglish: 'Naya request submit karein' },
  sv_request_type: { en: 'Request type', hi: 'अनुरोध प्रकार', hinglish: 'Request type' },
  sv_notes_optional: { en: 'Notes (optional)', hi: 'नोट्स (वैकल्पिक)', hinglish: 'Notes (optional)' },
  sv_submit_btn: { en: 'Submit Request', hi: 'अनुरोध सबमिट करें', hinglish: 'Request Submit Karein' },
  sv_submitting: { en: 'Submitting...', hi: 'सबमिट हो रहा है...', hinglish: 'Submit ho raha hai...' },
  sv_note: {
    en: 'Only the minimum information needed to track your request is stored - no sensitive banking details are saved in the receipt vault.',
    hi: 'केवल आपके अनुरोध को ट्रैक करने के लिए आवश्यक न्यूनतम जानकारी संग्रहीत की जाती है - रसीद वॉल्ट में कोई संवेदनशील बैंकिंग विवरण सहेजा नहीं जाता।',
    hinglish: 'Sirf request track karne ke liye zaroori minimum information store hoti hai - receipt vault mein koi sensitive banking detail save nahi hoti.',
  },
  sv_your_requests: { en: 'Your requests', hi: 'आपके अनुरोध', hinglish: 'Aapke requests' },
  sv_loading: { en: 'Loading your requests...', hi: 'आपके अनुरोध लोड हो रहे हैं...', hinglish: 'Aapke requests load ho rahe hain...' },
  sv_empty: { en: 'No requests yet. Submit one to get started.', hi: 'अभी तक कोई अनुरोध नहीं है। शुरू करने के लिए एक सबमिट करें।', hinglish: 'Abhi tak koi request nahi hai. Shuru karne ke liye ek submit karein.' },

  // --- Token / appointment ---
  tk_disclaimer: {
    en: 'This is a prototype digital queue system for demonstration only. It is not connected to any real bank branch or core banking system.',
    hi: 'यह केवल प्रदर्शन के लिए एक प्रोटोटाइप डिजिटल क्यू सिस्टम है। यह किसी वास्तविक बैंक शाखा या कोर बैंकिंग सिस्टम से जुड़ा नहीं है।',
    hinglish: 'Yeh sirf demonstration ke liye ek prototype digital queue system hai. Yeh kisi real bank branch ya core banking system se connected nahi hai.',
  },
  tk_request_token: { en: 'Request a token', hi: 'टोकन का अनुरोध करें', hinglish: 'Token request karein' },
  tk_branch: { en: 'Branch', hi: 'शाखा', hinglish: 'Branch' },
  tk_service: { en: 'Service', hi: 'सेवा', hinglish: 'Service' },
  tk_request_btn: { en: 'Request Token', hi: 'टोकन का अनुरोध करें', hinglish: 'Token Request Karein' },
  tk_requesting: { en: 'Requesting...', hi: 'अनुरोध हो रहा है...', hinglish: 'Request ho raha hai...' },
  tk_your_tokens: { en: 'Your tokens', hi: 'आपके टोकन', hinglish: 'Aapke tokens' },
  tk_loading: { en: 'Loading your tokens...', hi: 'आपके टोकन लोड हो रहे हैं...', hinglish: 'Aapke tokens load ho rahe hain...' },
  tk_empty: { en: 'No tokens requested yet.', hi: 'अभी तक कोई टोकन नहीं मांगा गया।', hinglish: 'Abhi tak koi token request nahi kiya gaya.' },
  tk_queue_position: { en: 'Queue position', hi: 'क्यू में स्थिति', hinglish: 'Queue position' },

  // --- Employee dashboard ---
  emp_total: { en: 'Total Requests', hi: 'कुल अनुरोध', hinglish: 'Total Requests' },
  emp_pending: { en: 'Pending', hi: 'लंबित', hinglish: 'Pending' },
  emp_completed: { en: 'Completed', hi: 'पूर्ण', hinglish: 'Completed' },
  emp_empty: { en: 'No customer requests yet.', hi: 'अभी तक कोई ग्राहक अनुरोध नहीं है।', hinglish: 'Abhi tak koi customer request nahi hai.' },
  emp_missing_docs: { en: 'Missing documents', hi: 'छूटे हुए दस्तावेज़', hinglish: 'Missing documents' },
  emp_validation_alerts: { en: 'Validation alerts', hi: 'सत्यापन अलर्ट', hinglish: 'Validation alerts' },
  emp_all_good: { en: 'Nothing outstanding for this request.', hi: 'इस अनुरोध के लिए कुछ भी बाकी नहीं है।', hinglish: 'Is request ke liye kuch bhi baaki nahi hai.' },

  // --- Generic ---
  loading: { en: 'Loading...', hi: 'लोड हो रहा है...', hinglish: 'Load ho raha hai...' },
  try_again: { en: 'Try again', hi: 'फिर से कोशिश करें', hinglish: 'Phir se try karein' },
}
