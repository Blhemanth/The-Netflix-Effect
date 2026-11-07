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
    print("STARTING COMPREHENSIVE BLACK-BOX TEST SUITE FOR NETFLIX DATA STORY ENGINE")
    print("=" * 70)
    
    app_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "app.py"))
    
    # -------------------------------------------------------------------------
    # BB-01: Navigation Test across all 5 pages
    # -------------------------------------------------------------------------
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
        "📖 Data Storytelling Report"
    ]
    
    for page in pages:
        at.sidebar.radio[0].set_value(page).run()
        assert not at.exception, f"Exception on {page}: {at.exception}"
        print(f"[PASS] Navigated to '{page}' - 0 exceptions.")
        
    # -------------------------------------------------------------------------
    # BB-02: Empty Maturity Ratings Selection (Boundary Value Analysis)
    # -------------------------------------------------------------------------
    print("\n--- BB-02: Empty Maturity Ratings Selection ---")
    at.sidebar.radio[0].set_value("🏠 Overview & Metrics").run()
    # Deselect all ratings
    at.sidebar.multiselect[0].set_value([]).run()
    assert not at.exception, f"Exception when ratings empty: {at.exception}"
    
    print(f"Active multiselect value: {at.sidebar.multiselect[0].value}")
    warnings = [w.value for w in at.warning]
    print(f"Warnings present when ratings empty: {warnings}")
    assert any("No titles match your current filter combination" in str(w) for w in warnings), \
        "Expected empty filter warning when 0 ratings selected"
    print("[PASS] Clearing all maturity ratings triggers empty state guidance as expected.")

    # -------------------------------------------------------------------------
    # BB-03: Zero-match Filter Permutations (Equivalence Partitioning)
    # -------------------------------------------------------------------------
    print("\n--- BB-03: Zero-match Filter Permutations ---")
    # Reset multiselect back to default first
    default_ratings = ["TV-MA", "TV-14", "TV-PG", "R", "PG-13", "TV-Y7", "TV-Y"]
    at.sidebar.multiselect[0].set_value(default_ratings).run()
    
    # Set search query to non-existent title
    at.sidebar.text_input[0].set_value("nonexistent_title_xyz_12345").run()
    assert not at.exception, f"Exception on zero match search: {at.exception}"
    warnings = [w.value for w in at.warning]
    assert any("No titles match" in str(w) for w in warnings), "Expected empty-match warning when 0 titles match!"
    print("[PASS] Zero-match search rendered without exception and prompted user.")
    
    # -------------------------------------------------------------------------
    # BB-04: Special Characters & Whitespace in Search (Robustness / Fuzzing)
    # -------------------------------------------------------------------------
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
        "<script>alert(1)</script>"
    ]
    for q in special_queries:
        at.sidebar.text_input[0].set_value(q).run()
        assert not at.exception, f"Crash on search query '{q}': {at.exception}"
    print("[PASS] All special character and Unicode searches handled safely without regex crashes.")

    # -------------------------------------------------------------------------
    # BB-05: Reset All Filters Button (State Mutation Regression)
    # -------------------------------------------------------------------------
    print("\n--- BB-05: Reset All Filters Button ---")
    at.sidebar.selectbox[0].set_value("TV Show").run()
    at.sidebar.slider[0].set_value((2000, 2010)).run()
    at.sidebar.text_input[0].set_value("Lucifer").run()
    
    # Click reset button
    reset_btn = at.sidebar.button[0] # "🔄 Reset All Filters"
    reset_btn.click().run()
    assert not at.exception, f"Exception on reset button: {at.exception}"
    print(f"After Reset - Content Type: {at.sidebar.selectbox[0].value}, Year Range: {at.sidebar.slider[0].value}, Search: '{at.sidebar.text_input[0].value}'")
    assert at.sidebar.selectbox[0].value == "All", "Content type should be reset to All"
    assert at.sidebar.slider[0].value == (1925, 2021), "Year range should be reset to (1925, 2021)"
    assert at.sidebar.text_input[0].value == "", "Search query should be reset to empty"
    print("[PASS] 'Reset All Filters' restores all default values smoothly without instantiation error.")

    # -------------------------------------------------------------------------
    # BB-06: Title Spotlight HTML Escaping & Universal Selection
    # -------------------------------------------------------------------------
    print("\n--- BB-06: Title Spotlight Card Selection ---")
    at.sidebar.radio[0].set_value("🏠 Overview & Metrics").run()
    spotlight_box = at.selectbox[0] # spotlight_universal_select
    # Select a title with an ampersand or special characters
    special_title_choice = [opt for opt in spotlight_box.options if "&" in opt][0]
    spotlight_box.set_value(special_title_choice).run()
    assert not at.exception, f"Exception on title selection '{special_title_choice}': {at.exception}"
    print(f"[PASS] Title Spotlight successfully rendered title containing special chars: '{special_title_choice}'")

    # -------------------------------------------------------------------------
    # BB-07: EDA Dropdown & Visualizations Accessibility
    # -------------------------------------------------------------------------
    print("\n--- BB-07: EDA Dropdown & Visualizations Inspection ---")
    at.sidebar.radio[0].set_value("📊 Visualizations & EDA").run()
    eda_selectbox = at.selectbox[0]
    options = eda_selectbox.options
    print(f"Available EDA dropdown options ({len(options)} total):")
    for opt in options:
        eda_selectbox.set_value(opt).run()
        assert not at.exception, f"Exception selecting EDA option '{opt}': {at.exception}"
    print(f"[PASS] All {len(options)} EDA visualization views load with 0 exceptions.")

    # -------------------------------------------------------------------------
    # BB-08: Analytical Insights Tabs
    # -------------------------------------------------------------------------
    print("\n--- BB-08: Analytical Insights Tabs Navigation ---")
    at.sidebar.radio[0].set_value("💡 Analytical Insights").run()
    assert not at.exception, f"Exception on Analytical Insights page: {at.exception}"
    print("[PASS] Analytical Insights page loaded cleanly.")

    # -------------------------------------------------------------------------
    # BB-09: Actionable Recommendations
    # -------------------------------------------------------------------------
    print("\n--- BB-09: Actionable Recommendations Execution Matrix ---")
    at.sidebar.radio[0].set_value("🎯 Actionable Recommendations").run()
    assert not at.exception, f"Exception on Recommendations page: {at.exception}"
    print("[PASS] Actionable Recommendations page loaded cleanly.")

    # -------------------------------------------------------------------------
    # BB-10: Interactive Quiz on Page 5
    # -------------------------------------------------------------------------
    print("\n--- BB-10: Page 5 Interactive Quiz ---")
    at.sidebar.radio[0].set_value("📖 Data Storytelling Report").run()
    
    # Test Q1 correct answer
    q1_radio = at.radio[0]
    q1_radio.set_value("~69.6%").run()
    q1_btn = at.button[0] # "Check Answer for Q1"
    q1_btn.click().run()
    assert not at.exception, f"Exception on Q1 correct submit: {at.exception}"
    successes = [s.value for s in at.success]
    assert any("Correct" in str(s) for s in successes), "Expected success feedback for correct Q1 answer"
    
    # Test Q2 correct answer
    q2_radio = at.radio[1]
    q2_radio.set_value("Algorithmic cancellation thresholds if shows fail to hit 28-day subscriber acquisition benchmarks").run()
    q2_btn = at.button[1] # "Check Answer for Q2"
    q2_btn.click().run()
    assert not at.exception, f"Exception on Q2 submit: {at.exception}"
    
    # Check that composite score banner appears
    score_markdowns = [m.value for m in at.markdown if "Your Quiz Score" in str(m.value)]
    assert len(score_markdowns) > 0, "Expected Composite Quiz Score Banner to appear when both questions answered"
    print(f"[PASS] Composite score banner displayed: {score_markdowns[0][:60]}...")
    
    # Test Reset Quiz Answers button
    reset_quiz_btn = at.button[2]
    assert reset_quiz_btn.label == "🔄 Reset Quiz Answers", f"Expected reset button, found {reset_quiz_btn.label}"
    reset_quiz_btn.click().run()
    assert not at.exception, f"Exception on reset quiz: {at.exception}"
    print("[PASS] Interactive Quiz correctly handles answer grading, score tallying, and answer resets.")

    print("\n" + "=" * 70)
    print("ALL 10 BLACK-BOX TEST SUITES PASSED FLAWLESSLY WITH 0 EXCEPTIONS!")
    print("=" * 70)

if __name__ == "__main__":
    run_tests()
