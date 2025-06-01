import streamlit as st
from datetime import datetime
import json
import os
from fpdf import FPDF
import hashlib
from typing import Dict, List, Optional

# Page configuration
st.set_page_config(
    page_title="Smart Letter Generator",
    page_icon="✉️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .letter-output {
        background: #f8f9fa;
        padding: 2rem;
        border-radius: 10px;
        border-left: 5px solid #667eea;
        font-family: 'Times New Roman', serif;
        line-height: 1.6;
        white-space: pre-line;
        color: #333333;
    }
    .voice-button {
        background: linear-gradient(45deg, #FF6B6B, #4ECDC4);
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        cursor: pointer;
    }
    /* Improved input field styling */
    .stTextInput input, .stTextArea textarea, .stDateInput input, .stSelectbox select {
        background-color: #ffffff !important;  /* White background */
        color: #000000 !important;             /* Black text */
        border: 1px solid #cccccc !important;   /* Light gray border */
    }
    .stTextInput label, .stTextArea label, .stDateInput label, .stSelectbox label {
        color: #ffffff !important;             /* White label text */
    }
    /* Fix radio button text color */
    .stRadio label {
        color: #000000 !important;             /* Black text for radio buttons */
    }
    /* Optional: Add some padding and rounded corners */
    .stTextInput input, .stTextArea textarea, .stDateInput input, .stSelectbox select {
        padding: 8px 12px !important;
        border-radius: 4px !important;
    }
</style>
""", unsafe_allow_html=True)

class LetterGenerator:
    def __init__(self):
        self.letter_types = {
            "Application for Leave": self.leave_application_fields,
            "Internship Request Letter": self.internship_request_fields,
            "Job Application Letter": self.job_application_fields,
            "Resignation Letter": self.resignation_letter_fields,
            "Complaint Letter": self.complaint_letter_fields,
            "Appreciation Letter": self.appreciation_letter_fields
        }
    
    def leave_application_fields(self):
        """Fields specific to leave application"""
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Your Name*", key="leave_name")
            reason = st.text_area("Reason for Leave*", key="leave_reason", height=100)
            position = st.text_input("Your Position/Role", key="leave_position")
        with col2:
            from_date = st.date_input("From Date*", key="leave_from")
            to_date = st.date_input("To Date*", key="leave_to")
            organization = st.text_input("Organization/College Name*", key="leave_org")
            manager_name = st.text_input("Manager/Supervisor Name", key="leave_manager")
        
        return {
            "name": name, "reason": reason, "from_date": from_date,
            "to_date": to_date, "organization": organization,
            "position": position, "manager_name": manager_name
        }
    
    def internship_request_fields(self):
        """Fields specific to internship request"""
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Your Name*", key="intern_name")
            university = st.text_input("University/College*", key="intern_uni")
            course = st.text_input("Course/Major*", key="intern_course")
            email = st.text_input("Email Address*", key="intern_email")
        with col2:
            company = st.text_input("Company Name*", key="intern_company")
            duration = st.text_input("Internship Duration*", key="intern_duration")
            department = st.text_input("Preferred Department", key="intern_dept")
            skills = st.text_area("Relevant Skills", key="intern_skills", height=100)
        
        return {
            "name": name, "university": university, "course": course,
            "email": email, "company": company, "duration": duration,
            "department": department, "skills": skills
        }
    
    def job_application_fields(self):
        """Fields specific to job application"""
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Your Name*", key="job_name")
            position = st.text_input("Position Applied For*", key="job_position")
            experience = st.text_input("Years of Experience", key="job_exp")
            email = st.text_input("Email Address*", key="job_email")
        with col2:
            company = st.text_input("Company Name*", key="job_company")
            phone = st.text_input("Phone Number", key="job_phone")
            qualifications = st.text_area("Key Qualifications", key="job_qual", height=100)
            reference = st.text_input("How did you hear about this position?", key="job_ref")
        
        return {
            "name": name, "position": position, "experience": experience,
            "email": email, "company": company, "phone": phone,
            "qualifications": qualifications, "reference": reference
        }
    
    def resignation_letter_fields(self):
        """Fields specific to resignation letter"""
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Your Name*", key="resign_name")
            position = st.text_input("Your Current Position*", key="resign_position")
            last_day = st.date_input("Last Working Day*", key="resign_last_day")
        with col2:
            manager_name = st.text_input("Manager/Supervisor Name*", key="resign_manager")
            company = st.text_input("Company Name*", key="resign_company")
            reason = st.text_area("Reason for Leaving (Optional)", key="resign_reason", height=100)
        
        return {
            "name": name, "position": position, "last_day": last_day,
            "manager_name": manager_name, "company": company, "reason": reason
        }
    
    def complaint_letter_fields(self):
        """Fields specific to complaint letter"""
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Your Name*", key="complaint_name")
            recipient = st.text_input("Recipient Name/Department*", key="complaint_recipient")
            issue = st.text_area("Issue/Problem*", key="complaint_issue", height=120)
        with col2:
            organization = st.text_input("Organization/Company", key="complaint_org")
            date_occurred = st.date_input("When did this occur?", key="complaint_date")
            resolution = st.text_area("Desired Resolution", key="complaint_resolution", height=120)
        
        return {
            "name": name, "recipient": recipient, "issue": issue,
            "organization": organization, "date_occurred": date_occurred,
            "resolution": resolution
        }
    
    def appreciation_letter_fields(self):
        """Fields specific to appreciation letter"""
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Your Name*", key="appreciation_name")
            recipient = st.text_input("Recipient Name*", key="appreciation_recipient")
            achievement = st.text_area("What are you appreciating?*", key="appreciation_achievement", height=120)
        with col2:
            organization = st.text_input("Organization/Company", key="appreciation_org")
            relationship = st.text_input("Your relationship to recipient", key="appreciation_relationship")
            impact = st.text_area("Impact of their work/action", key="appreciation_impact", height=120)
        
        return {
            "name": name, "recipient": recipient, "achievement": achievement,
            "organization": organization, "relationship": relationship, "impact": impact
        }

class LetterTemplates:
    @staticmethod
    def generate_leave_application(data, style="standard"):
        """Generate leave application letter"""
        date_str = datetime.now().strftime("%B %d, %Y")
        
        if style == "professional":
            letter = f"""Date: {date_str}

To: {data.get('manager_name', 'The Manager')}
{data['organization']}

Subject: Application for Leave - {data['from_date']} to {data['to_date']}

Dear Sir/Madam,

I am writing to formally request leave from my duties as {data.get('position', 'employee')} for the period from {data['from_date']} to {data['to_date']}.

The reason for my leave request is {data['reason']}. I have ensured that all my current responsibilities will be appropriately managed during my absence, and I will coordinate with my colleagues to ensure minimal disruption to ongoing projects.

I would be grateful if you could approve my leave request. I am committed to completing any urgent tasks before my departure and will ensure a smooth transition of my responsibilities.

Thank you for your consideration of this request. I look forward to your positive response.

Respectfully yours,

{data['name']}
{data.get('position', '')}"""
        
        elif style == "short":
            letter = f"""Date: {date_str}

To: {data.get('manager_name', 'Manager')}
{data['organization']}

Subject: Leave Request - {data['from_date']} to {data['to_date']}

Dear {data.get('manager_name', 'Sir/Madam')},

I request leave from {data['from_date']} to {data['to_date']} due to {data['reason']}.

I will ensure all pending work is completed before my leave.

Please approve my request.

Thanks,
{data['name']}"""
        
        else:  # standard
            letter = f"""Date: {date_str}

To: {data.get('manager_name', 'The Manager')}
{data['organization']}

Subject: Application for Leave

Dear {data.get('manager_name', 'Sir/Madam')},

I hope this letter finds you well. I am writing to request leave from my position as {data.get('position', 'employee')} from {data['from_date']} to {data['to_date']}.

The reason for my leave is {data['reason']}. I will make sure to complete all my pending tasks and coordinate with my team members to ensure smooth operations during my absence.

I would appreciate your approval for this leave request. Please let me know if you need any additional information.

Thank you for your understanding.

Sincerely,
{data['name']}"""
        
        return letter
    
    @staticmethod
    def generate_internship_request(data, style="standard"):
        """Generate internship request letter"""
        date_str = datetime.now().strftime("%B %d, %Y")
        
        if style == "professional":
            letter = f"""Date: {date_str}

To: The Human Resources Department
{data['company']}

Subject: Application for Internship Opportunity - {data.get('department', 'Various Departments')}

Dear Hiring Manager,

I am {data['name']}, currently pursuing {data['course']} at {data['university']}. I am writing to express my strong interest in securing an internship position at {data['company']} for a duration of {data['duration']}.

Your organization's reputation for excellence and innovation in the industry has inspired me to seek this opportunity to contribute to your team while gaining valuable practical experience. My academic background in {data['course']}, combined with my skills in {data.get('skills', 'various areas')}, positions me well to contribute meaningfully to your organization.

I am particularly interested in working with the {data.get('department', 'team')} department, where I believe I can apply my theoretical knowledge while learning from industry professionals. I am eager to bring fresh perspectives and dedication to any projects or initiatives I would be involved in.

I have attached my resume for your review and would welcome the opportunity to discuss how I can contribute to your organization. I am flexible with timing and committed to making the most of this learning opportunity.

Thank you for considering my application. I look forward to hearing from you.

Sincerely,

{data['name']}
{data['email']}
{data['university']}"""
        
        elif style == "short":
            letter = f"""Date: {date_str}

To: HR Department
{data['company']}

Subject: Internship Application

Dear Sir/Madam,

I am {data['name']}, a {data['course']} student at {data['university']}.

I would like to apply for an internship at {data['company']} for {data['duration']}. I have skills in {data.get('skills', 'relevant areas')} and am eager to gain practical experience.

Please consider my application.

Contact: {data['email']}

Thanks,
{data['name']}"""
        
        else:  # standard
            letter = f"""Date: {date_str}

To: The Hiring Team
{data['company']}

Subject: Internship Application

Dear Sir/Madam,

My name is {data['name']}, and I am currently a student of {data['course']} at {data['university']}. I am writing to apply for an internship opportunity at {data['company']}.

I am very interested in gaining practical experience in the field and believe that {data['company']} would provide an excellent learning environment. I would like to intern for {data['duration']} and am particularly interested in the {data.get('department', 'relevant')} department.

My skills include {data.get('skills', 'various technical and soft skills')}, which I believe would be valuable to your team. I am hardworking, eager to learn, and committed to contributing positively to your organization.

I would be grateful for the opportunity to discuss my application further. Please find my contact information below.

Thank you for your time and consideration.

Best regards,
{data['name']}
Email: {data['email']}"""
        
        return letter
    
    @staticmethod
    def generate_job_application(data, style="standard"):
        """Generate job application letter"""
        date_str = datetime.now().strftime("%B %d, %Y")
        
        if style == "professional":
            letter = f"""Date: {date_str}

To: The Hiring Manager
{data['company']}

Subject: Application for {data['position']} Position

Dear Hiring Manager,

I am writing to express my strong interest in the {data['position']} position at {data['company']}. With {data.get('experience', 'relevant')} years of experience in the field, I am confident that my skills and expertise align perfectly with your requirements.

{data.get('reference', 'I learned about this opportunity through your company website')}, and I was immediately drawn to {data['company']}'s reputation for excellence and innovation. Your organization's commitment to quality and growth resonates with my professional values and career aspirations.

My key qualifications include:
{data.get('qualifications', 'Strong technical skills and proven track record of success')}

I have consistently demonstrated the ability to deliver results, work collaboratively with diverse teams, and adapt to evolving business needs. I am particularly excited about the opportunity to contribute to {data['company']}'s continued success while advancing my own professional development.

I have attached my resume for your detailed review and would welcome the opportunity to discuss how my background and enthusiasm can benefit your team. I am available for an interview at your convenience and can be reached at {data.get('phone', 'the provided contact information')} or {data['email']}.

Thank you for your time and consideration. I look forward to hearing from you soon.

Sincerely,

{data['name']}
{data['email']}
{data.get('phone', '')}"""
        
        elif style == "short":
            letter = f"""Date: {date_str}

To: Hiring Team
{data['company']}

Subject: {data['position']} Application

Dear Hiring Manager,

I'm applying for the {data['position']} role at {data['company']}.

Experience: {data.get('experience', 'Relevant')} years
Key skills: {data.get('qualifications', 'Various professional skills')}

I'm interested in contributing to your team and would appreciate an interview opportunity.

Contact: {data['email']}, {data.get('phone', '')}

Best regards,
{data['name']}"""
        
        else:  # standard
            letter = f"""Date: {date_str}

To: The Hiring Team
{data['company']}

Subject: Application for {data['position']}

Dear Hiring Manager,

I am interested in applying for the {data['position']} position at {data['company']}. {data.get('reference', 'I found this opportunity online')} and believe my background makes me a strong candidate.

I have {data.get('experience', 'relevant')} years of experience and possess the following qualifications:
{data.get('qualifications', 'Strong professional skills and dedication to excellence')}

I am excited about the opportunity to work with {data['company']} and contribute to your team's success. I am confident that my skills and enthusiasm would be valuable assets to your organization.

Please find my resume attached. I would welcome the opportunity to discuss my application in more detail.

Thank you for your consideration.

Best regards,
{data['name']}
Email: {data['email']}
Phone: {data.get('phone', '')}"""
        
        return letter
    
    @staticmethod
    def generate_resignation_letter(data, style="standard"):
        """Generate resignation letter"""
        date_str = datetime.now().strftime("%B %d, %Y")
        
        if style == "professional":
            letter = f"""Date: {date_str}

To: {data['manager_name']}
{data['company']}

Subject: Formal Resignation from Position of {data['position']}

Dear {data['manager_name']},

I am writing to formally notify you of my resignation from my position as {data['position']} at {data['company']}. My last day of employment will be {data['last_day']}, providing the standard notice period.

{f"After careful consideration, I have decided to resign due to {data['reason']}." if data.get('reason') else "This decision was not made lightly and comes after careful consideration of my career goals and personal circumstances."}

I am committed to ensuring a smooth transition during my remaining time with the company. I will do everything possible to complete my current projects and assist in training my replacement or transitioning my responsibilities to other team members.

I want to express my sincere gratitude for the opportunities for professional and personal growth that I have experienced during my tenure at {data['company']}. The knowledge and experience I have gained here will be invaluable throughout my career.

Please let me know how I can be of assistance during this transition period. I am happy to help recruit and train my replacement to ensure continuity in my role.

Thank you for your understanding. I wish {data['company']} and the entire team continued success.

Respectfully,

{data['name']}
{data['position']}"""
        
        elif style == "short":
            letter = f"""Date: {date_str}

To: {data['manager_name']}
{data['company']}

Subject: Resignation Notice

Dear {data['manager_name']},

I am resigning from my position as {data['position']}. My last working day will be {data['last_day']}.

{f"Reason: {data['reason']}" if data.get('reason') else ""}

I will ensure proper handover of my responsibilities.

Thank you for the opportunities provided.

Regards,
{data['name']}"""
        
        else:  # standard
            letter = f"""Date: {date_str}

To: {data['manager_name']}
{data['company']}

Subject: Resignation from {data['position']} Position

Dear {data['manager_name']},

I am writing to inform you that I am resigning from my position as {data['position']} at {data['company']}. My last day of work will be {data['last_day']}.

{f"I have made this decision because {data['reason']}." if data.get('reason') else "This was a difficult decision for me to make."}

I will do my best to complete my current projects and help with the transition of my responsibilities. I am willing to assist in training my replacement if needed.

I want to thank you and the team for the support and opportunities provided during my time here. I have learned a lot and enjoyed working with everyone.

Please let me know how I can help make this transition as smooth as possible.

Thank you for your understanding.

Sincerely,
{data['name']}"""
        
        return letter
    
    @staticmethod
    def generate_complaint_letter(data, style="standard"):
        """Generate complaint letter"""
        date_str = datetime.now().strftime("%B %d, %Y")
        
        if style == "professional":
            letter = f"""Date: {date_str}

To: {data['recipient']}
{data.get('organization', '')}

Subject: Formal Complaint Regarding {data['issue'][:50]}...

Dear {data['recipient']},

I am writing to bring to your attention a serious concern that requires immediate attention and resolution. On {data.get('date_occurred', 'recently')}, I experienced the following issue:

{data['issue']}

This matter has caused significant inconvenience and concern, and I believe it requires prompt action to prevent similar occurrences in the future. The situation not only affects me personally but potentially impacts other stakeholders as well.

I have attempted to resolve this matter through informal channels, but the issue persists, necessitating this formal complaint. I believe that {data.get('organization', 'your organization')} maintains high standards of service and professionalism, which is why I am confident that appropriate action will be taken.

To resolve this matter satisfactorily, I would appreciate the following:
{data.get('resolution', 'A thorough investigation of the issue and appropriate corrective measures')}

I trust that you will treat this complaint with the seriousness it deserves and take swift action to address the concerns raised. I look forward to your prompt response within a reasonable timeframe.

Should you require any additional information or clarification regarding this matter, please do not hesitate to contact me.

Thank you for your attention to this matter.

Sincerely,

{data['name']}"""
        
        elif style == "short":
            letter = f"""Date: {date_str}

To: {data['recipient']}

Subject: Complaint - {data['issue'][:30]}...

Dear {data['recipient']},

I am writing to complain about: {data['issue']}

This occurred on {data.get('date_occurred', 'recently')} and needs immediate attention.

Resolution needed: {data.get('resolution', 'Appropriate action to fix this issue')}

Please address this promptly.

{data['name']}"""
        
        else:  # standard
            letter = f"""Date: {date_str}

To: {data['recipient']}
{data.get('organization', '')}

Subject: Complaint Regarding {data['issue'][:40]}...

Dear {data['recipient']},

I hope this letter finds you well. I am writing to express my concern about an issue that occurred on {data.get('date_occurred', 'recently')}.

The problem I encountered is as follows:
{data['issue']}

This situation has caused me considerable inconvenience and I believe it needs to be addressed promptly. I trust that {data.get('organization', 'your organization')} values customer satisfaction and will take appropriate action.

To resolve this matter, I would appreciate:
{data.get('resolution', 'A satisfactory solution to prevent this from happening again')}

I hope we can resolve this matter quickly and amicably. Please let me know what steps will be taken to address my concerns.

Thank you for your time and attention.

Sincerely,
{data['name']}"""
        
        return letter
    
    @staticmethod
    def generate_appreciation_letter(data, style="standard"):
        """Generate appreciation letter"""
        date_str = datetime.now().strftime("%B %d, %Y")
        
        if style == "professional":
            letter = f"""Date: {date_str}

To: {data['recipient']}
{data.get('organization', '')}

Subject: Recognition and Appreciation for Outstanding Performance

Dear {data['recipient']},

I am writing to formally express my sincere appreciation and recognition for your exceptional work and dedication. As {data.get('relationship', 'someone who has observed your work')}, I felt compelled to acknowledge your outstanding contributions.

Specifically, I would like to commend you for:
{data['achievement']}

Your efforts have had a significant positive impact:
{data.get('impact', 'Your work has made a meaningful difference to our team and organization')}

Your professionalism, commitment to excellence, and positive attitude serve as an inspiration to others. The quality of your work and your dedication to achieving results consistently exceed expectations and contribute significantly to our collective success.

Please know that your hard work and contributions are noticed and deeply valued. It is a privilege to work with someone of your caliber, and I wanted to ensure that your efforts receive the recognition they deserve.

Thank you once again for your outstanding work and continued dedication. I look forward to our continued collaboration and your future contributions.

With sincere appreciation,

{data['name']}
{data.get('relationship', '')}"""
        
        elif style == "short":
            letter = f"""Date: {date_str}

To: {data['recipient']}

Subject: Thank You and Appreciation

Dear {data['recipient']},

I wanted to thank you for {data['achievement']}.

{data.get('impact', 'Your efforts made a real difference')} and I really appreciate your hard work.

Keep up the excellent work!

Best regards,
{data['name']}"""
        
        else:  # standard
            letter = f"""Date: {date_str}

To: {data['recipient']}
{data.get('organization', '')}

Subject: Appreciation and Thanks

Dear {data['recipient']},

I hope you are doing well. I wanted to take a moment to express my heartfelt appreciation for your excellent work.

I am particularly impressed by:
{data['achievement']}

{data.get('impact', 'Your contribution has made a positive impact')} and I wanted to make sure you know how much it is valued and appreciated.

Thank you for your dedication and hard work. It's people like you who make a real difference, and I feel fortunate to {data.get('relationship', 'work with you')}.

Please keep up the fantastic work!

With gratitude,
{data['name']}"""
        
        return letter

class PDFGenerator:
    def create_pdf(self, letter_content, filename="letter.pdf"):
        """Create PDF from letter content"""
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        
        # Split content into lines and add to PDF
        lines = letter_content.split('\n')
        for line in lines:
            # Handle long lines by wrapping them
            if len(line) > 80:
                words = line.split(' ')
                current_line = ""
                for word in words:
                    if len(current_line + word) < 80:
                        current_line += word + " "
                    else:
                        pdf.cell(200, 10, txt=current_line.strip(), ln=True, align='L')
                        current_line = word + " "
                if current_line:
                    pdf.cell(200, 10, txt=current_line.strip(), ln=True, align='L')
            else:
                pdf.cell(200, 10, txt=line, ln=True, align='L')
        
        # Convert bytearray to bytes
        return bytes(pdf.output(dest='S'))

class UserManager:
    def __init__(self):
        self.users_file = "users.json"
        self.load_users()
    
    def load_users(self):
        """Load users from file"""
        if os.path.exists(self.users_file):
            with open(self.users_file, 'r') as f:
                self.users = json.load(f)
        else:
            self.users = {}
    
    def save_users(self):
        """Save users to file"""
        with open(self.users_file, 'w') as f:
            json.dump(self.users, f)
    
    def hash_password(self, password):
        """Hash password for security"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def register_user(self, username, password, email, full_name):
        """Register new user"""
        if username in self.users:
            return False, "Username already exists"
        
        self.users[username] = {
            "password": self.hash_password(password),
            "email": email,
            "full_name": full_name,
            "templates": {},
            "created_at": datetime.now().isoformat()
        }
        self.save_users()
        return True, "User registered successfully"
    
    def login_user(self, username, password):
        """Login user"""
        if username not in self.users:
            return False, "Username not found"
        
        if self.users[username]["password"] != self.hash_password(password):
            return False, "Invalid password"
        
        return True, "Login successful"
    
    def get_user_templates(self, username):
        """Get user's saved templates"""
        if username in self.users:
            return self.users[username].get("templates", {})
        return {}
    
    def save_user_template(self, username, template_name, template_data):
        """Save user template"""
        if username in self.users:
            if "templates" not in self.users[username]:
                self.users[username]["templates"] = {}
            self.users[username]["templates"][template_name] = template_data
            self.save_users()
            return True
        return False

def main():
    # Initialize session state
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "username" not in st.session_state:
        st.session_state.username = ""
    if "generated_letter" not in st.session_state:
        st.session_state.generated_letter = ""
    
    # Initialize classes
    letter_gen = LetterGenerator()
    templates = LetterTemplates()
    pdf_gen = PDFGenerator()
    user_manager = UserManager()
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>✉️ Smart Letter Generator</h1>
        <p>Generate professional letters with customizable templates</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar for login/register
    with st.sidebar:
        st.header("👤 User Account")
        
        if not st.session_state.logged_in:
            tab1, tab2 = st.tabs(["Login", "Register"])
            
            with tab1:
                st.subheader("Login")
                login_username = st.text_input("Username", key="login_user")
                login_password = st.text_input("Password", type="password", key="login_pass")
                login_button = st.button("Login")
                
                if login_button:
                    if not login_username or not login_password:
                        st.error("Please enter both username and password")
                    else:
                        success, message = user_manager.login_user(login_username, login_password)
                        if success:
                            st.session_state.logged_in = True
                            st.session_state.username = login_username
                            st.success(message)
                            st.rerun()
                        else:
                            st.error(message)
            
            with tab2:
                st.subheader("Register")
                reg_username = st.text_input("Choose a username", key="reg_user")
                reg_password = st.text_input("Choose a password", type="password", key="reg_pass")
                reg_email = st.text_input("Email address", key="reg_email")
                reg_fullname = st.text_input("Full name", key="reg_name")
                register_button = st.button("Register")
                
                if register_button:
                    if not reg_username or not reg_password or not reg_email or not reg_fullname:
                        st.error("Please fill all fields")
                    else:
                        success, message = user_manager.register_user(
                            reg_username, reg_password, reg_email, reg_fullname
                        )
                        if success:
                            st.success(message)
                        else:
                            st.error(message)
        else:
            st.success(f"Logged in as {st.session_state.username}")
            if st.button("Logout"):
                st.session_state.logged_in = False
                st.session_state.username = ""
                st.session_state.generated_letter = ""
                st.rerun()
            
            # User templates section
            st.subheader("📁 Saved Templates")
            user_templates = user_manager.get_user_templates(st.session_state.username)
            
            if user_templates:
                selected_template = st.selectbox(
                    "Your templates",
                    options=list(user_templates.keys()),
                    key="user_template_select"
                )
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Load Template"):
                        template_data = user_templates[selected_template]
                        st.session_state.generated_letter = template_data["content"]
                        st.rerun()
                with col2:
                    if st.button("Delete Template", type="secondary"):
                        del user_manager.users[st.session_state.username]["templates"][selected_template]
                        user_manager.save_users()
                        st.success("Template deleted")
                        st.rerun()
            else:
                st.info("No saved templates yet")
    
    # Main content area
    if st.session_state.logged_in:
        # Letter type selection
        col1, col2 = st.columns([3, 1])
        with col1:
            letter_type = st.selectbox(
                "Select Letter Type",
                options=list(letter_gen.letter_types.keys()),
                key="letter_type"
            )
        with col2:
            letter_style = st.selectbox(
                "Letter Style",
                options=["standard", "professional", "short"],
                key="letter_style"
            )
        
        # Get fields based on letter type
        field_function = letter_gen.letter_types[letter_type]
        letter_data = field_function()
        
        # Generate letter button
        if st.button("Generate Letter", type="primary"):
            # Validate required fields
            required_fields = [k for k, v in letter_data.items() if v == "" or v is None]
            if required_fields:
                st.error(f"Please fill all required fields: {', '.join(required_fields)}")
            else:
                # Generate the letter based on type and style
                if letter_type == "Application for Leave":
                    letter_content = templates.generate_leave_application(letter_data, letter_style)
                elif letter_type == "Internship Request Letter":
                    letter_content = templates.generate_internship_request(letter_data, letter_style)
                elif letter_type == "Job Application Letter":
                    letter_content = templates.generate_job_application(letter_data, letter_style)
                elif letter_type == "Resignation Letter":
                    letter_content = templates.generate_resignation_letter(letter_data, letter_style)
                elif letter_type == "Complaint Letter":
                    letter_content = templates.generate_complaint_letter(letter_data, letter_style)
                elif letter_type == "Appreciation Letter":
                    letter_content = templates.generate_appreciation_letter(letter_data, letter_style)
                
                st.session_state.generated_letter = letter_content
        
        # Display generated letter
        if st.session_state.generated_letter:
            st.subheader("Generated Letter")
            st.markdown(
                f'<div class="letter-output">{st.session_state.generated_letter}</div>',
                unsafe_allow_html=True
            )
            
            # Letter actions
            col1, col2, col3 = st.columns([1, 1, 2])
            with col1:
                # Download as PDF
                pdf_bytes = pdf_gen.create_pdf(st.session_state.generated_letter)
                st.download_button(
                    label="Download as PDF",
                    data=pdf_bytes,
                    file_name="generated_letter.pdf",
                    mime="application/pdf"
                )
            with col2:
                # Copy to clipboard
                if st.button("Copy to Clipboard"):
                    st.markdown(f"""
                    <script>
                        navigator.clipboard.writeText(`{st.session_state.generated_letter.replace("`", "\\`").replace("\n", "\\n")}`);
                        alert("Letter copied to clipboard!");
                    </script>
                    """, unsafe_allow_html=True)
                    st.success("Copied to clipboard!")
            with col3:
                # Save as template
                template_name = st.text_input("Save as template", key="template_name")
                if st.button("Save Template") and template_name:
                    user_manager.save_user_template(
                        st.session_state.username,
                        template_name,
                        {
                            "type": letter_type,
                            "style": letter_style,
                            "content": st.session_state.generated_letter,
                            "data": letter_data,
                            "created_at": datetime.now().isoformat()
                        }
                    )
                    st.success("Template saved!")
    else:
        st.info("Please login or register to use the Letter Generator")
        st.markdown("""
        ### Features:
        - Generate professional letters in seconds
        - Multiple letter types and styles
        - Save and manage your templates
        - Download as PDF
        
        Register now to get started!
        """)

if __name__ == "__main__":
    main()
