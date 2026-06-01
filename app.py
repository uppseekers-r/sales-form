import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime

# ==========================================
# 1. DATABASE INITIALIZATION & STRUCTURE
# ==========================================
def init_db():
    conn = sqlite3.connect("sales_pipeline.db", check_same_thread=False)
    cursor = conn.cursor()
    
    # Access control / Users table
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
        email TEXT PRIMARY KEY,
        password TEXT,
        access_level TEXT
    )''')
    
    # Student Master Profile Table
    cursor.execute('''CREATE TABLE IF NOT EXISTS students (
        email TEXT PRIMARY KEY,
        name TEXT,
        number TEXT,
        city TEXT,
        grade TEXT,
        school TEXT,
        school_board TEXT,
        intake_year TEXT,
        mother_name TEXT,
        mother_number TEXT,
        mother_email TEXT,
        mother_occ TEXT,
        father_name TEXT,
        father_number TEXT,
        father_email TEXT,
        father_occ TEXT,
        desired_universities TEXT,
        desired_careers TEXT,
        desired_countries TEXT,
        services_taken TEXT,
        total_revenue REAL,
        payment_type TEXT,
        amount_received REAL,
        pending_dues REAL,
        remarks_counselor TEXT,
        remarks_ops TEXT,
        remarks_sales TEXT
    )''')
    
    # Detailed Installments Booking Sub-Table
    cursor.execute('''CREATE TABLE IF NOT EXISTS installments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_email TEXT,
        installment_number INTEGER,
        due_date TEXT,
        amount REAL,
        status TEXT,
        payment_id TEXT,
        payment_mode TEXT
    )''')
    
    # Default Admin Acc Seed
    cursor.execute("INSERT OR IGNORE INTO users VALUES ('admin@uppseekers.com', 'Uppseekers@2026', 'admin')")
    conn.commit()
    return conn

conn = init_db()

# ==========================================
# 2. APPLICATION ROUTING & STATE MANAGEMENT
# ==========================================
st.set_page_config(page_title="Uppseekers Client Database", layout="wide")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_email = ""
    st.session_state.access_level = ""

# --- Authentication Gateway Layout ---
if not st.session_state.logged_in:
    st.title("🔑 Uppseekers Corporate Registry Dashboard")
    st.write("Welcome to the internal sales pipeline. Please log in below.")
    
    login_email = st.text_input("Corporate Email Address")
    login_password = st.text_input("Access Password", type="password")
    
    if st.button("Unlock Core Dashboard", use_container_width=True):
        cursor = conn.cursor()
        cursor.execute("SELECT access_level FROM users WHERE email=? AND password=?", (login_email, login_password))
        result = cursor.fetchone()
        if result:
            st.session_state.logged_in = True
            st.session_state.user_email = login_email
            st.session_state.access_level = result[0]
            st.success("Access Granted. Booting modules...")
            st.rerun()
        else:
            st.error("Invalid credentials or unassigned authorization status.")
    st.stop()

# --- Top App Workspace Actions ---
st.sidebar.title(f"💼 Portal Node")
st.sidebar.info(f"User: {st.session_state.user_email}\nRole: {st.session_state.access_level.upper()}")

if st.sidebar.button("Secure Logout"):
    st.session_state.logged_in = False
    st.rerun()

# --- Main Business Workflow ---
menu = st.tabs(["📝 Intake & Pipeline Desk", "📊 Global Management Panel", "👥 Team Credentials Manager"])

# ==========================================
# 3. TAB 1: ENTRY & CONTEXT-DEPENDENT REDIRECTS
# ==========================================
with menu[0]:
    st.header("Section 1 - Initial Registry Context Allocation")
    
    # Common Parameters
    sales_advisor = st.text_input("Sales Advisor / Representative Name", value=st.session_state.user_email)
    
    customer_category = st.radio(
        "Type of Customer Activity Context",
        [
            "Category 1 - New Student Onboarding Registry",
            "Category 2 - Existing Student Profile (Upselling Entry)",
            "Category 3 - Existing Student Profile (Installment Processing Desk)"
        ]
    )
    
    st.markdown("---")
    
    # ----------------------------------------
    # SUB-SECTION 2A: NEW STUDENT PIPELINE
    # ----------------------------------------
    if "Category 1" in customer_category:
        st.subheader("Section 2a - New Candidate Master Profile Breakdown")
        
        col1, col2 = st.columns(2)
        with col1:
            s_name = st.text_input("Student Legal First & Last Name")
            s_phone = st.text_input("Primary Contact Mobile Number")
            s_email = st.text_input("Unique Candidate System Email (Primary Key)")
            s_city = st.text_input("Residential / Base City")
        with col2:
            s_grade = st.selectbox("Current Academic Grade Standard", ["Grade 6", "Grade 7", "Grade 8", "Grade 9", "Grade 10", "Grade 11", "Grade 12", "Undergrad"])
            s_school = st.text_input("Institution / School Name")
            s_board = st.selectbox("Affiliated School Board Matrix", ["Stateboard", "CBSE", "ICSE", "IGCSE", "IB"])
            s_intake = st.selectbox("Target Academic Intake Timeline Horizon", [f"Fall {year}" for year in range(2027, 2034)])
            
        st.markdown("#### Parent/Guardian Structural Nodes")
        pcol1, pcol2 = st.columns(2)
        with pcol1:
            m_name = st.text_input("Mother's Full Name")
            m_phone = st.text_input("Mother's Contact Number")
            m_email = st.text_input("Mother's Email Address")
            m_occ = st.text_input("Mother's Professional Occupation")
        with pcol2:
            f_name = st.text_input("Father's Full Name")
            f_phone = st.text_input("Father's Contact Number")
            f_email = st.text_input("Father's Email Address")
            f_occ = st.text_input("Father's Professional Occupation")
            
        st.markdown("#### Desired Matrix Targets (Provide up to 5 entries for each category, comma-separated)")
        d1, d2, d3 = st.columns(3)
        with d1:
            desired_uni = st.text_area("Target University Targets", placeholder="e.g., Harvard, NUS, Oxford")
        with d2:
            desired_car = st.text_area("Target Core Career Horizons", placeholder="e.g., Tech/AI, Finance, Bio-tech")
        with d3:
            desired_cnt = st.text_area("Desired Country Targets", placeholder="e.g., US, UK, Singapore")
            
        st.markdown("---")
        st.subheader("Section 3a - Curated Program/Package Allocation Details")
        services_taken = st.multiselect(
            "What functional operational segments are taken from us?",
            ["ICP", "Counseling", "Research", "Short Internship", "Long Internship", "Project", "SAT"]
        )
        
        rem_counselor = st.text_area("Counselor Interface Reference Notes")
        rem_ops = st.text_area("Operations Team Allocation Notes")
        rem_sales = st.text_area("Sales Team Master Notes & Reference Logs")
        
        st.markdown("---")
        st.subheader("Section 4 - Fiscal/Revenue Allocation Framework")
        total_revenue = st.number_input("Total Closed Contract Revenue Valuation (INR)", min_value=0.0, step=1000.0)
        payment_type = st.selectbox("Settlement Structure Mode Selection", ["Full Payment", "Installments"])
        
        installment_count = 0
        installment_data = []
        if payment_type == "Installments":
            st.info("💡 Map the prospective milestone timeline tracking below (Max 5 items allowed as per organizational standard protocol).")
            for i in range(1, 6):
                st.markdown(f"**Milestone Frame Entry #{i}**")
                icol1, icol2 = st.columns(2)
                with icol1:
                    idate = st.date_input(f"Scheduled Execution Date Target for Installment {i}", key=f"new_idate_{i}")
                with icol2:
                    iamt = st.number_input(f"Expected Financial Volume Valuation for Installment {i} (INR)", min_value=0.0, step=500.0, key=f"new_iamt_{i}")
                if iamt > 0:
                    installment_data.append((i, idate.strftime("%Y-%m-%d"), iamt))
                    
        st.markdown("#### Instant Session Collection Snapshot Receipt Details")
        rcol1, rcol2, rcol3 = st.columns(3)
        with rcol1:
            amt_rec = st.number_input("Amount Collected Immediately in Current Session Frame (INR)", min_value=0.0, step=1000.0)
        with rcol2:
            pay_id = st.text_input("Transaction / Gateway Payment ID Token")
        with rcol3:
            pay_mode = st.selectbox("Validated Financial Settlement Channel", ["Razorpay", "Bank Transfer", "Cash / Direct Check"])
            
        screenshot_mock = st.file_uploader("Upload Verification Image / Payment Reference Document Screenshot", type=["png", "jpg", "jpeg", "pdf"])
        
        # Calculate Pends automatically
        pending_dues = total_revenue - amt_rec
        st.metric("Automatically Calculated Outstanding Balance Deficit", f"INR {pending_dues:,.2f}")
        
        if st.button("Finalize and Save New Record Profile to Database", use_container_width=True):
            if not s_email or not s_name:
                st.error("Missing mandatory fields. Candidate Identity Email & Candidate Name fields must be set.")
            else:
                try:
                    cursor = conn.cursor()
                    cursor.execute("""
                        INSERT INTO students VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                    """, (
                        s_email, s_name, s_phone, s_city, s_grade, s_school, s_board, s_intake,
                        m_name, m_phone, m_email, m_occ, f_name, f_phone, f_email, f_occ,
                        desired_uni, desired_car, desired_cnt, ",".join(services_taken),
                        total_revenue, payment_type, amt_rec, pending_dues, rem_counselor, rem_ops, rem_sales
                    ))
                    
                    # Log mapping frames for future collections if selected
                    for idx, d_dt, d_am in installment_data:
                        # Mark first installment as processed dynamically if payment completely covers it
                        status_label = "Pending"
                        cursor.execute("INSERT INTO installments (student_email, installment_number, due_date, amount, status) VALUES (?,?,?,?,?)",
                                       (s_email, idx, d_dt, d_am, status_label))
                        
                    conn.commit()
                    st.success(f"Success! Master Profile Node for {s_name} successfully appended to system.")
                except sqlite3.IntegrityError:
                    st.error("Critical: A profile utilizing this student email address already exists.")

    # ----------------------------------------
    # SUB-SECTION 2B: EXSITING STUDENT (UPSELLING)
    # ----------------------------------------
    elif "Category 2" in customer_category:
        st.subheader("Section 2b - Upselling Validation Engine Workspace")
        
        # Fetch Student Records
        cursor = conn.cursor()
        cursor.execute("SELECT email, name FROM students")
        existing_students = cursor.fetchall()
        
        if not existing_students:
            st.warning("No student registry arrays currently parsed in database.")
        else:
            student_mapping = {f"{r[1]} ({r[0]})": r[0] for r in existing_students}
            selected_student_key = st.selectbox("Select Target Existing Student Matrix Node", list(student_mapping.keys()))
            target_email = student_mapping[selected_student_key]
            
            # Fetch previous records snapshot
            cursor.execute("SELECT services_taken, total_revenue, pending_dues, remarks_sales FROM students WHERE email=?", (target_email,))
            st_data = cursor.fetchone()
            
            st.info(f"📋 **Current Services Enrolled:** {st_data[0]} | **Contract Historical Base Revenue:** INR {st_data[1]:,.2f} | **Outstanding Dues:** INR {st_data[2]:,.2f}")
            
            st.markdown("#### Append Upselled Services Contract Adjustments")
            upsell_services = st.multiselect(
                "Select Additional Services Being Upsold to Student Node",
                ["ICP", "Counseling", "Research", "Short Internship", "Long Internship", "Project", "SAT"],
                key="upsell_serv"
            )
            
            additional_revenue = st.number_input("Incremental Contract Expansion Revenue Value (INR)", min_value=0.0, step=1000.0)
            upsell_remarks = st.text_area("Append Extra Sales Operational Activity Log Entry Notes")
            
            if st.button("Apply Upsell Adjustment Record Updates to Node", use_container_width=True):
                new_services_set = list(set((st_data[0].split(",") if st_data[0] else []) + upsell_services))
                new_revenue = st_data[1] + additional_revenue
                new_dues = st_data[2] + additional_revenue
                new_remarks = f"{st_data[3]}\n[{datetime.now().strftime('%Y-%m-%d')}] Upsell Action Note: {upsell_remarks}"
                
                cursor.execute("""
                    UPDATE students 
                    SET services_taken=?, total_revenue=?, pending_dues=?, remarks_sales=? 
                    WHERE email=?
                """, (",".join(new_services_set), new_revenue, new_dues, new_remarks, target_email))
                conn.commit()
                st.success("Upsell adjustments compiled and written to database ledger.")
                st.rerun()

    # ----------------------------------------
    # SUB-SECTION 2C: INSTALLMENT RE-ENTRY PROCESSING
    # ----------------------------------------
    elif "Category 3" in customer_category:
        st.subheader("Section 2c - Active Installment Ledger Reconciliation Desk")
        
        cursor = conn.cursor()
        cursor.execute("SELECT email, name FROM students")
        existing_students = cursor.fetchall()
        
        if not existing_students:
            st.warning("No structural profile configurations available to process.")
        else:
            student_mapping = {f"{r[1]} ({r[0]})": r[0] for r in existing_students}
            selected_student_key = st.selectbox("Select Target Profile Node for Balance Reconciliation", list(student_mapping.keys()))
            target_email = student_mapping[selected_student_key]
            
            # Fetch Current State Metrics
            cursor.execute("SELECT total_revenue, amount_received, pending_dues, remarks_sales FROM students WHERE email=?", (target_email,))
            m_rev, m_rec, m_due, m_rem = cursor.fetchone()
            
            col1, col2, col3 = st.columns(3)
            col1.metric("Historical Booked Contract Value", f"INR {m_rev:,.2f}")
            col2.metric("Accumulated Collections Received", f"INR {m_rec:,.2f}")
            col3.metric("Current Tracked Outstanding Balances", f"INR {m_due:,.2f}", delta="- Actionable Dues")
            
            # Show scheduled items ledger if matching subtable frame exists
            cursor.execute("SELECT installment_number, due_date, amount, status FROM installments WHERE student_email=?", (target_email,))
            inst_records = cursor.fetchall()
            if inst_records:
                st.markdown("#### Programmed Milestone Mapping Reference Table")
                df_inst = pd.DataFrame(inst_records, columns=["Installment No", "Target Due Date", "Expected Amount Value", "Current Status"])
                st.table(df_inst)
            
            st.markdown("---")
            st.markdown("#### Input New Collection Event Transaction Values")
            
            cc1, cc2 = st.columns(2)
            with cc1:
                amt_paid_now = st.number_input("Amount Collected in Current Session Activity (INR)", min_value=0.0, max_value=float(m_due), step=1000.0)
                pay_id_now = st.text_input("Session Reference Transaction ID / Gateway Code")
            with cc2:
                pay_mode_now = st.selectbox("Financial Node Settlement Mode", ["Razorpay", "Bank Transfer", "Direct Counter Deposit"])
                extra_dues_adj = st.number_input("Add Extra Fine / Miscellaneous Late Dues Expansion (If Any)", min_value=0.0, step=100.0)
                
            session_screenshot = st.file_uploader("Upload Session Ledger Receipt Image Reference", type=["png", "jpg", "jpeg", "pdf"], key="sess_screen")
            post_pay_remarks = st.text_area("Append Post-Payment Sales Ledger Verification Commentary Notes")
            
            if st.button("Apply Collection Event Token & Balance Reconciliation", use_container_width=True):
                updated_rec = m_rec + amt_paid_now
                updated_due = (m_due - amt_paid_now) + extra_dues_adj
                updated_remarks = f"{m_rem}\n[{datetime.now().strftime('%Y-%m-%d')}] Processed collection payment frame of INR {amt_paid_now:,.2f} via {pay_mode_now}. Notes: {post_pay_remarks}"
                
                # If there are installments, mark the earliest "Pending" one as paid
                cursor.execute("""
                    UPDATE installments 
                    SET status='PAID', payment_id=?, payment_mode=? 
                    WHERE id = (
                        SELECT id FROM installments 
                        WHERE student_email=? AND status='Pending' 
                        ORDER BY installment_number ASC LIMIT 1
                    )
                """, (pay_id_now, pay_mode_now, target_email))
                
                # Update main student master node record
                cursor.execute("""
                    UPDATE students 
                    SET amount_received=?, pending_dues=?, remarks_sales=? 
                    WHERE email=?
                """, (updated_rec, updated_due, updated_remarks, target_email))
                
                conn.commit()
                st.success("Ledger array values updated. Account reconciled.")
                st.rerun()

# ==========================================
# 4. TAB 2: MANAGEMENT COMPREHENSIVE VIEW
# ==========================================
with menu[1]:
    st.header("Global Operational Registry Pipeline Summary Data View")
    
    cursor = conn.cursor()
    cursor.execute("SELECT email, name, grade, school_board, total_revenue, amount_received, pending_dues, services_taken FROM students")
    all_students_raw = cursor.fetchall()
    
    if not all_students_raw:
        st.info("No active pipeline data clusters found in localized data infrastructure system.")
    else:
        df_master = pd.DataFrame(all_students_raw, columns=[
            "System Email ID", "Student Name", "Grade Standard", "Affiliated Board Cluster", 
            "Booked Revenue Pool", "Collections Liquidated", "Outstanding Dues Left", "Enrolled Services"
        ])
        
        # Display Key Summary Operational Financial Metrics Data Card Panels
        st.markdown("#### High-Level Pipeline Revenue Financial Metrics Analytics Dashboard")
        mcol1, mcol2, mcol3 = st.columns(3)
        mcol1.metric("Gross Total Enrolled Closed Contract Pipeline Value", f"INR {df_master['Booked Revenue Pool'].sum():,.2f}")
        mcol2.metric("Total Liquid Assets Net Liquidated Value Secured", f"INR {df_master['Collections Liquidated'].sum():,.2f}")
        mcol3.metric("Aggregate Accounts Receivable Pipeline Bookings Outstanding", f"INR {df_master['Outstanding Dues Left'].sum():,.2f}")
        
        st.markdown("---")
        st.dataframe(df_master, use_container_width=True)
        
        # Advanced Inspection Deep Dive Selector
        st.markdown("### Profile Complete Database Inspection View Node")
        inspect_mapping = {f"{row[1]} ({row[0]})": row[0] for row in all_students_raw}
        inspect_target = st.selectbox("Choose Targeted Student Object Mapping File For Data Analysis Room", list(inspect_mapping.keys()))
        
        if inspect_target:
            t_email = inspect_mapping[inspect_target]
            cursor.execute("SELECT * FROM students WHERE email=?", (t_email,))
            full_record = cursor.fetchone()
            
            # Display formatted details clean
            st.json({
                "Student Identity Node": {
                    "Name": full_record[1], "Phone Reference": full_record[2], "Email": full_record[0],
                    "City Zone Location": full_record[3], "Current Class Grade": full_record[4],
                    "Target School Matrix Node": full_record[5], "Board Layout Selection": full_record[6],
                    "Intake Horizon": full_record[7]
                },
                "Kinship/Guardian Data Nodes": {
                    "Mother Information Matrix": f"Name: {full_record[8]} | Contact: {full_record[9]} | Email: {full_record[10]} | Professional Focus: {full_record[11]}",
                    "Father Information Matrix": f"Name: {full_record[12]} | Contact: {full_record[13]} | Email: {full_record[14]} | Professional Focus: {full_record[15]}"
                },
                "Strategic Intent Parameters": {
                    "Desired Universities Matrix Target Setup": full_record[16],
                    "Desired Track Careers Choice Target Setup": full_record[17],
                    "Desired Country Geographical Focus Set": full_record[18]
                },
                "System Administrative Operational Commentary Notes Logs": {
                    "Counselor Workspace Direct Notes": full_record[24],
                    "Operations Functional Queue Notes": full_record[25],
                    "Sales Activity Reconciliation Logs": full_record[26]
                }
            })

# ==========================================
# 5. TAB 3: TEAM ACCESS MANAGEMENT
# ==========================================
with menu[2]:
    st.header("Team Authorization Control Console Engine Room")
    if st.session_state.access_level != "admin":
        st.warning("Security Protocol Exception. Access Restricted exclusively to root admin administrative privileges.")
    else:
        st.markdown("#### Authorize New Operational Team Member Access Identity Node")
        new_user_email = st.text_input("New Representative User Team Login Email ID String")
        new_user_pass = st.text_input("Set Team Representative Access Password Token String", type="password")
        new_user_role = st.selectbox("Define Role Functional Access Authorization Matrix Scope Level", ["manager", "sales_rep"])
        
        if st.button("Generate & Register Corporate Account Node", use_container_width=True):
            if new_user_email and new_user_pass:
                cursor = conn.cursor()
                cursor.execute("INSERT OR REPLACE INTO users VALUES (?,?,?)", (new_user_email, new_user_pass, new_user_role))
                conn.commit()
                st.success(f"System Record Access Authorization Node Written Successfully for user: {new_user_email}")
            else:
                st.error("Input validation schema structural assignment mismatch parameters missing fields.")
