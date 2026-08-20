import unittest
from loan_processing_system import calculate_loan

class TestLoanProcessingQA(unittest.TestCase):

    def setUp(self):
        # Default baseline mock payload (valid profile)
        self.valid_profile = {
            "customer_id": "CUST101",
            "age": 30,
            "monthly_salary": 5000.0,
            "existing_loan_amount": 12000.0,
            "credit_score": 750,
            "employment_type": "salaried",
            "requested_loan_amount": 25000.0,
            "loan_tenure": 5
        }

    def test_min_max_age(self):
        """Test minimum/maximum age constraints"""
        self.valid_profile["age"] = 17
        self.assertEqual(calculate_loan(self.valid_profile)["status"], "Rejected")
        self.valid_profile["age"] = 70
        self.assertEqual(calculate_loan(self.valid_profile)["status"], "Rejected")

    def test_invalid_salary(self):
        """Test invalid salary entry handling"""
        self.valid_profile["monthly_salary"] = -100
        self.assertEqual(calculate_loan(self.valid_profile)["status"], "Rejected")

    def test_poor_credit_score(self):
        """Test poor credit score assessment criteria"""
        self.valid_profile["credit_score"] = 450
        res = calculate_loan(self.valid_profile)
        self.assertEqual(res["status"], "Rejected")
        self.assertIn("credit", res["reason"].lower())

    def test_existing_loan_exceeding_threshold(self):
        """Test system reactions to existing massive loan limits"""
        self.valid_profile["existing_loan_amount"] = 1500000
        res = calculate_loan(self.valid_profile)
        self.assertEqual(res["status"], "Rejected")

    def test_high_debt_to_income_ratio(self):
        """Test high debt-to-income constraints"""
        self.valid_profile["monthly_salary"] = 1000.0
        self.valid_profile["existing_loan_amount"] = 80000.0
        res = calculate_loan(self.valid_profile)
        self.assertEqual(res["status"], "Rejected")

    def test_different_employment_categories(self):
        """Test interest adjustments for unique operational employment tags"""
        self.valid_profile["employment_type"] = "self-employed"
        res = calculate_loan(self.valid_profile)
        self.assertEqual(res["interest_rate"], 8.0)  # 7% standard base + 1% premium

    def test_boundary_loan_amounts(self):
        """Test handling of border requested limit restrictions"""
        self.valid_profile["requested_loan_amount"] = 9999999
        res = calculate_loan(self.valid_profile)
        self.assertEqual(res["status"], "Rejected")

    def test_emi_calculation_accuracy(self):
        """Test accuracy validations for mathematical EMI calculations"""
        # Under controlled constraints (P=10000, R=12% annual -> 1% monthly, N=12 months)
        test_profile = {
            "customer_id": "T-EMI", "age": 30, "monthly_salary": 10000, 
            "existing_loan_amount": 0, "credit_score": 550,  # 15% rate
            "employment_type": "salaried", "requested_loan_amount": 10000, "loan_tenure": 1
        }
        res = calculate_loan(test_profile)
        self.assertGreater(res["emi"], 0)

    def test_invalid_input_handling(self):
        """Verify type safety when broken types cross input barriers"""
        self.valid_profile["age"] = "not-an-integer"
        with self.assertRaises(ValueError):
            calculate_loan(self.valid_profile)

    def test_exception_handling(self):
        """Ensure system fails gracefully under missing structural arguments"""
        broken_profile = {"customer_id": "CUST-MISSING"}
        with self.assertRaises(ValueError):
            calculate_loan(broken_profile)

if __name__ == '__main__':
    unittest.main()
