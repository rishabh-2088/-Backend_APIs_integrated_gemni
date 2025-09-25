import pytest
from app import score_lead_rules

# Sample offer data for testing
offer = {
    "name": "AI Outreach Automation",
    "value_props": ["24/7 outreach", "6x more meetings"],
    "ideal_use_cases": ["b2b saas"]  # Lowercased to match .lower() comparisons
}

# Test cases for role relevance, industry match, and data completeness
@pytest.mark.parametrize("lead, expected_score", [
    # Test case 1: 20 (decision maker) + 20 (industry match) + 10 (complete) = 50
    ({
        "name": "Ava Patel", 
        "role": "Head of Growth", 
        "company": "FlowMetrics",
        "industry": "B2B SaaS", 
        "location": "New York", 
        "linkedin_bio": "Growth leader"
    }, 50),
      
    # Test case 2: 10 (influencer) + 20 (industry match) + 10 = 40
    ({
        "name": "Ben Carter", 
        "role": "Senior Marketing Manager", 
        "company": "Innovate Corp",
        "industry": "B2B SaaS", 
        "location": "London", 
        "linkedin_bio": "Driving strategies"
    }, 40),

    # Test case 3: 0 (no role match) + 0 (no industry match) + 0 (incomplete) = 0
    ({
        "name": "Dan Smith", 
        "role": "Intern", 
        "company": "Acme Inc",
        "industry": "Education", 
        "location": "Austin", 
        "linkedin_bio": ""
    }, 0),

    # Test case 4: 20 (decision maker) + 20 (industry match) + 0 (incomplete) = 40
    ({
        "name": "Incomplete Data", 
        "role": "VP of Sales", 
        "company": "Incomplete",
        "industry": "B2B SaaS", 
        "location": "Chicago"  # Missing 'linkedin_bio' (incomplete)
    }, 40),
])
def test_score_lead_rules(lead, expected_score):
    """
    Tests the rule-based scoring logic with various lead inputs.
    """
    actual_score = score_lead_rules(lead, offer)
    assert actual_score == expected_score, f"Expected {expected_score}, got {actual_score} for lead: {lead}"
