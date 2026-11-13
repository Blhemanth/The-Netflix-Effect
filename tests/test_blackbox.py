import sys
import os
import io

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass
import pandas as pd
from streamlit.testing.v1 import AppTest

def run_tests():
    print("=" * 70)
    print("STARTING BLACK-BOX TEST SUITE FOR NETFLIX DATA STORY ENGINE")
    print("=" * 70)
    
    app_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "app.py"))
    
    # BB-01: Navigation Test across all 5 pages
    print("\n--- BB-01: Navigation Across All 5 Pages ---")
    at = AppTest.from_file(app_path, default_timeout=15)
    at.run()
    assert not at.exception, f"Default load exception: {at.exception}"
    print("[PASS] Default load (Page 1) rendered with 0 exceptions.")
    
    pages = [
        "🏠 Overview & Metrics",
        "📊 Visualizations & EDA",
        "💡 Analytical Insights",
        "🎯 Actionable Recommendations",
        "🔮 Future Predictions (What-If Studio)",
        "📖 Data Storytelling Report"
    ]
    
    for page in pages:
        at.sidebar.radio[0].set_value(page).run()
        assert not at.exception, f"Exception on {page}: {at.exception}"
        print(f"[PASS] Navigated to '{page}' - 0 exceptions.")
        
    # BB-02: Empty Maturity Ratings Selection
    print("\n--- BB-02: Empty Maturity Ratings Selection ---")
    at.sidebar.radio[0].set_value("🏠 Overview & Metrics").run()
    # Deselect all ratings
    at.sidebar.multiselect[0].set_value([]).run()
    assert not at.exception, f"Exception when ratings empty: {at.exception}"
    
    # Check what is displayed
    print(f"Active multiselect value: {at.sidebar.multiselect[0].value}")
    warnings = [w.value for w in at.warning]
    print(f"Warnings present when ratings empty: {warnings}")

    
    # BB-03: Zero-match Filter Permutations
    print("\n--- BB-03: Zero-match Filter Permutations ---")
    # Set search query to non-existent title
    at.sidebar.text_input[0].set_value("nonexistent_title_xyz_12345").run()
    assert not at.exception, f"Exception on zero match search: {at.exception}"
    print("[PASS] Zero-match search rendered without exception.")
    
    # Verify zero match shows warning
    warnings = [w.value for w in at.warning]
    print(f"Zero match warnings: {warnings}")
    assert any("No titles match" in str(w) for w in warnings), "Expected empty-match warning when 0 titles match!"
    print("[PASS] User receives clear warning when filter yields 0 titles.")
    
    # BB-04: Special Characters & Whitespace in Search
    print("\n--- BB-04: Special Characters & Whitespace in Search ---")
    special_queries = [
        "   Stranger Things   ",
        "[test]",
        "a+b",
        "*",
        "?",
        "\"quote\"",
        "Élite",
        "100%",
        "<script>"
    ]
    for q in special_queries:
        at.sidebar.text_input[0].set_value(q).run()
        assert not at.exception, f"Crash on search query '{q}': {at.exception}"
    print("[PASS] All special character and Unicode searches handled safely without regex crashes.")

    # BB-05: Reset All Filters Button
    print("\n--- BB-05: Reset All Filters Button ---")
    # Change multiple filters
    at.sidebar.selectbox[0].set_value("TV Show").run()
    at.sidebar.slider[0].set_value((2000, 2010)).run()
    at.sidebar.text_input[0].set_value("Lucifer").run()
    
    # Click reset button (st.button in expander)
    reset_btn = at.sidebar.button[0] # "🔄 Reset All Filters"
    reset_btn.click().run()
    assert not at.exception, f"Exception on reset button: {at.exception}"
    print(f"After Reset - Content Type: {at.sidebar.selectbox[0].value}, Year Range: {at.sidebar.slider[0].value}, Search: '{at.sidebar.text_input[0].value}'")
    assert at.sidebar.selectbox[0].value == "All", "Content type should be reset to All"
    assert at.sidebar.slider[0].value == (1925, 2021), "Year range should be reset to (1925, 2021)"
    assert at.sidebar.text_input[0].value == "", "Search query should be reset to empty"
    print("[PASS] 'Reset All Filters' restores all default values accurately.")

    # BB-06: EDA Dropdown & Visualizations Accessibility
    print("\n--- BB-06: EDA Dropdown & Visualizations Inspection ---")
    at.radio[0].set_value("📊 Visualizations & EDA").run()
    eda_selectbox = at.selectbox[0]
    options = eda_selectbox.options
    print(f"Available EDA dropdown options ({len(options)} total):")
    for opt in options:
        eda_selectbox.set_value(opt).run()
        assert not at.exception, f"Exception selecting EDA option '{opt}': {at.exception}"
    print(f"[PASS] All {len(options)} EDA visualization views load with 0 exceptions.")

    # BB-07: Interactive Quiz on Page 5
    print("\n--- BB-07: Page 5 Interactive Quiz ---")
    at.sidebar.radio[0].set_value("📖 Data Storytelling Report").run()
    
    # Test Q1 correct answer
    q1_radio = at.main.radio[0]
    q1_radio.set_value("~69.6%").run()
    q1_btn = at.main.button[0] # "Check Answer for Q1"
    q1_btn.click().run()
    assert not at.exception, f"Exception on Q1 correct submit: {at.exception}"
    successes = [s.value for s in at.success]
    print(f"Q1 success message: {successes}")
    assert any("Correct" in str(s) for s in successes), "Expected success feedback for correct Q1 answer"
    
    # Test Q2 wrong answer
    q2_radio = at.main.radio[1]
    q2_radio.set_value("Directors refuse to film second seasons").run()
    q2_btn = at.main.button[1] # "Check Answer for Q2"
    q2_btn.click().run()
    assert not at.exception, f"Exception on Q2 submit: {at.exception}"
    errors = [e.value for e in at.error]
    print(f"Q2 error message: {errors}")
    assert any("Incorrect" in str(e) or "Not quite" in str(e) for e in errors), "Expected error feedback for wrong Q2 answer"
    
    # Test Reset Quiz Answers button
    reset_quiz_btn = at.main.button[2]
    assert reset_quiz_btn.label == "🔄 Reset Quiz Answers", f"Expected reset button, found {reset_quiz_btn.label}"
    reset_quiz_btn.click().run()
    assert not at.exception, f"Exception on reset quiz: {at.exception}"
    print("[PASS] Interactive Quiz correctly handles correct answers, incorrect answers, and answer resets.")

    # BB-08: Future Predictions (What-If Studio) Power BI Interactivity
    print("\n--- BB-08: Future Predictions (What-If Studio) Power BI Testing ---")
    at.sidebar.radio[0].set_value("🔮 Future Predictions (What-If Studio)").run()
    assert not at.exception, f"Exception loading Future Predictions page: {at.exception}"
    print("[PASS] '🔮 Future Predictions (What-If Studio)' loaded with 0 exceptions.")
    
    # Check scenario preset switching on main page
    preset_sb = at.main.selectbox[0] # The Scenario Preset selector in main area
    scenarios = preset_sb.options
    for sc in scenarios:
        preset_sb.set_value(sc).run()
        assert not at.exception, f"Exception switching scenario to '{sc}': {at.exception}"
    print(f"[PASS] Successfully cycled through all {len(scenarios)} prediction scenarios: {scenarios}")

    # Test What-If Hit Simulator interaction
    sim_btn = [b for b in at.main.button if "Simulate Title Performance" in str(b.label)]
    if sim_btn:
        sim_btn[0].click().run()
        assert not at.exception, f"Exception clicking Hit Simulator: {at.exception}"
        print("[PASS] Title Popularity Simulator evaluated and rendered predictions successfully.")

    print("\n" + "=" * 70)
    print("ALL INITIAL BLACK-BOX AUTOMATED TESTS EXECUTED!")
    print("=" * 70)

if __name__ == "__main__":
    run_tests()
