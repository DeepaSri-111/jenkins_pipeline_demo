import math

def calculate_loan(data):
    """
    Validates inputs and calculates loan criteria for Banking Loan Approval System.
    """
    # 1. Input Handling & Exception Handling Checks
    try:
        customer_id = str(data['customer_id'])
        age = int(data['age'])
        monthly_salary = float(data['monthly_salary'])
        existing_loan_amt = float(data['existing_loan_amount'])
        credit_score = int(data['credit_score'])
        employment_type = str(data['employment_type']).lower()
        requested_amt = float(data['requested_loan_amount'])
        tenure_years = int(data['loan_tenure'])
    except (ValueError, TypeError, KeyError) as e:
        raise ValueError(f"Invalid input handling triggered: {str(e)}")

    # Age rules
    if age < 18 or age > 65:
        return {"status": "Rejected", "reason": "Age outside minimum/maximum limits"}
        
    # Salary rules
    if monthly_salary <= 0:
        return {"status": "Rejected", "reason": "Invalid salary amount"}

    # 2. Calculations
    # Debt-to-Income (DTI) Ratio (Simulated calculation with existing loan monthly obligation estimation)
    estimated_existing_emi = existing_loan_amt / 120  # assumption
    dti_ratio = (estimated_existing_emi / monthly_salary) * 100

    # Base interest rate by employment type and credit score
    if credit_score < 600:
        base_rate = 0.15  # Poor credit score penalty
    elif credit_score < 750:
        base_rate = 0.10
    else:
        base_rate = 0.07

    if employment_type == "self-employed":
        base_rate += 0.01  # Employment premium

    # EMI calculation: [P x R x (1+R)^N]/[(1+R)^N-1]
    monthly_rate = base_rate / 12
    months = tenure_years * 12
    
    if requested_amt > 0 and months > 0:
        emi = (requested_amt * monthly_rate * (1 + monthly_rate)**months) / ((1 + monthly_rate)**months - 1)
    else:
        emi = 0.0

    # Eligible loan amount limits based on salary & credit
    max_eligible = monthly_salary * 50 if credit_score >= 700 else monthly_salary * 30

    # 3. Decision Logic Matrix
    if credit_score < 500:
        status = "Rejected"
        reason = "Poor credit score"
    elif existing_loan_amt > 1000000:
        status = "Rejected"
        reason = "Existing loan exceeding threshold"
    elif dti_ratio > 50:
        status = "Rejected"
        reason = "High debt-to-income ratio"
    elif requested_amt > max_eligible:
        status = "Rejected"
        reason = "Requested amount exceeds eligible loan amount"
    else:
        status = "Approved"
        reason = "Passed all standard criteria"

    return {
        "customer_id": customer_id,
        "dti_ratio": round(dti_ratio, 2),
        "eligible_loan_amount": round(max_eligible, 2),
        "interest_rate": round(base_rate * 100, 2),
        "emi": round(emi, 2),
        "status": status,
        "reason": reason
    }
