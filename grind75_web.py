import streamlit as st
import json
import os
import time
import pandas as pd
from datetime import datetime, timedelta

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Grind 75 Daily Check-in",
    page_icon="🔥",
    layout="wide"
)

# --- STYLING ---
st.markdown("""
<style>
    /* Compact Buttons for Traffic Light feel */
    .stButton button { 
        width: 100%; 
        border-radius: 20px; 
        font-weight: bold; 
        border: none;
        padding: 5px 10px;
    }
    
    /* Custom Stats Cards */
    .stat-card {
        background-color: #262730; 
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        border: 1px solid #464b5c;
        margin-bottom: 20px;
    }
    .stat-value { font-size: 32px; font-weight: bold; margin: 0; }
    .stat-label { font-size: 14px; color: #a0a0a0; margin: 0; }
    
    /* Specific Colors */
    .color-green { color: #4ade80; } 
    .color-yellow { color: #facc15; } 
    .color-gray { color: #9ca3af; }   
    
    /* Streak Banner */
    .streak-container {
        padding: 15px;
        border-radius: 10px;
        background: linear-gradient(90deg, #ff4b1f 0%, #ff9068 100%);
        color: white;
        text-align: center;
        margin-bottom: 25px;
        font-weight: bold;
    }

    /* Remove excessive padding from dividers */
    hr { margin-top: 5px; margin-bottom: 5px; }
    
    /* Timer Style */
    .timer-box {
        padding: 10px;
        border: 1px solid #464b5c;
        border-radius: 8px;
        text-align: center;
        margin-bottom: 10px;
        background-color: #1e1e1e;
    }
    
    @media (prefers-color-scheme: light) {
        .stat-card { background-color: #ffffff; border: 1px solid #e0e0e0; }
        .timer-box { background-color: #f0f2f6; border: 1px solid #ccc; }
    }
</style>
""", unsafe_allow_html=True)

# --- DATA ---
INITIAL_PROBLEMS = [
  # Arrays & Hashing
  { "id": 1, "title": "Two Sum", "difficulty": "Easy", "topic": "Arrays & Hashing", "link": "https://leetcode.com/problems/two-sum/" },
  { "id": 2, "title": "Valid Anagram", "difficulty": "Easy", "topic": "Arrays & Hashing", "link": "https://leetcode.com/problems/valid-anagram/" },
  { "id": 3, "title": "Contains Duplicate", "difficulty": "Easy", "topic": "Arrays & Hashing", "link": "https://leetcode.com/problems/contains-duplicate/" },
  { "id": 4, "title": "Group Anagrams", "difficulty": "Medium", "topic": "Arrays & Hashing", "link": "https://leetcode.com/problems/group-anagrams/" },
  { "id": 5, "title": "Top K Frequent Elements", "difficulty": "Medium", "topic": "Arrays & Hashing", "link": "https://leetcode.com/problems/top-k-frequent-elements/" },
  { "id": 6, "title": "Product of Array Except Self", "difficulty": "Medium", "topic": "Arrays & Hashing", "link": "https://leetcode.com/problems/product-of-array-except-self/" },
  { "id": 7, "title": "Longest Consecutive Sequence", "difficulty": "Medium", "topic": "Arrays & Hashing", "link": "https://leetcode.com/problems/longest-consecutive-sequence/" },
  { "id": 56, "title": "Valid Sudoku", "difficulty": "Medium", "topic": "Arrays & Hashing", "link": "https://leetcode.com/problems/valid-sudoku/" },
  { "id": 57, "title": "Sort Colors", "difficulty": "Medium", "topic": "Arrays & Hashing", "link": "https://leetcode.com/problems/sort-colors/" },
  
  # Two Pointers
  { "id": 8, "title": "Valid Palindrome", "difficulty": "Easy", "topic": "Two Pointers", "link": "https://leetcode.com/problems/valid-palindrome/" },
  { "id": 9, "title": "3Sum", "difficulty": "Medium", "topic": "Two Pointers", "link": "https://leetcode.com/problems/3sum/" },
  { "id": 10, "title": "Container With Most Water", "difficulty": "Medium", "topic": "Two Pointers", "link": "https://leetcode.com/problems/container-with-most-water/" },
  { "id": 75, "title": "Trapping Rain Water", "difficulty": "Hard", "topic": "Two Pointers", "link": "https://leetcode.com/problems/trapping-rain-water/" },
  
  # Sliding Window
  { "id": 11, "title": "Best Time to Buy and Sell Stock", "difficulty": "Easy", "topic": "Sliding Window", "link": "https://leetcode.com/problems/best-time-to-buy-and-sell-stock/" },
  { "id": 12, "title": "Longest Substring Without Repeating Characters", "difficulty": "Medium", "topic": "Sliding Window", "link": "https://leetcode.com/problems/longest-substring-without-repeating-characters/" },
  { "id": 13, "title": "Longest Repeating Character Replacement", "difficulty": "Medium", "topic": "Sliding Window", "link": "https://leetcode.com/problems/longest-repeating-character-replacement/" },
  { "id": 64, "title": "Permutation in String", "difficulty": "Medium", "topic": "Sliding Window", "link": "https://leetcode.com/problems/permutation-in-string/" },
  { "id": 65, "title": "Minimum Window Substring", "difficulty": "Hard", "topic": "Sliding Window", "link": "https://leetcode.com/problems/minimum-window-substring/" },
  { "id": 66, "title": "Sliding Window Maximum", "difficulty": "Hard", "topic": "Sliding Window", "link": "https://leetcode.com/problems/sliding-window-maximum/" },

  # Stack
  { "id": 14, "title": "Valid Parentheses", "difficulty": "Easy", "topic": "Stack", "link": "https://leetcode.com/problems/valid-parentheses/" },
  { "id": 15, "title": "Min Stack", "difficulty": "Medium", "topic": "Stack", "link": "https://leetcode.com/problems/min-stack/" },
  { "id": 16, "title": "Evaluate Reverse Polish Notation", "difficulty": "Medium", "topic": "Stack", "link": "https://leetcode.com/problems/evaluate-reverse-polish-notation/" },
  { "id": 62, "title": "Daily Temperatures", "difficulty": "Medium", "topic": "Stack", "link": "https://leetcode.com/problems/daily-temperatures/" },
  { "id": 63, "title": "Largest Rectangle in Histogram", "difficulty": "Hard", "topic": "Stack", "link": "https://leetcode.com/problems/largest-rectangle-in-histogram/" },
  
  # Binary Search
  { "id": 17, "title": "Binary Search", "difficulty": "Easy", "topic": "Binary Search", "link": "https://leetcode.com/problems/binary-search/" },
  { "id": 18, "title": "Search a 2D Matrix", "difficulty": "Medium", "topic": "Binary Search", "link": "https://leetcode.com/problems/search-a-2d-matrix/" },
  { "id": 19, "title": "Find Minimum in Rotated Sorted Array", "difficulty": "Medium", "topic": "Binary Search", "link": "https://leetcode.com/problems/find-minimum-in-rotated-sorted-array/" },
  { "id": 20, "title": "Search in Rotated Sorted Array", "difficulty": "Medium", "topic": "Binary Search", "link": "https://leetcode.com/problems/search-in-rotated-sorted-array/" },
  { "id": 61, "title": "Time Based Key-Value Store", "difficulty": "Medium", "topic": "Binary Search", "link": "https://leetcode.com/problems/time-based-key-value-store/" },

  # Linked List
  { "id": 21, "title": "Reverse Linked List", "difficulty": "Easy", "topic": "Linked List", "link": "https://leetcode.com/problems/reverse-linked-list/" },
  { "id": 22, "title": "Merge Two Sorted Lists", "difficulty": "Easy", "topic": "Linked List", "link": "https://leetcode.com/problems/merge-two-sorted-lists/" },
  { "id": 23, "title": "Reorder List", "difficulty": "Medium", "topic": "Linked List", "link": "https://leetcode.com/problems/reorder-list/" },
  { "id": 24, "title": "Remove Nth Node From End of List", "difficulty": "Medium", "topic": "Linked List", "link": "https://leetcode.com/problems/remove-nth-node-from-end-of-list/" },
  { "id": 25, "title": "Linked List Cycle", "difficulty": "Easy", "topic": "Linked List", "link": "https://leetcode.com/problems/linked-list-cycle/" },
  { "id": 26, "title": "Merge k Sorted Lists", "difficulty": "Hard", "topic": "Linked List", "link": "https://leetcode.com/problems/merge-k-sorted-lists/" },
  
  # Trees
  { "id": 27, "title": "Invert Binary Tree", "difficulty": "Easy", "topic": "Trees", "link": "https://leetcode.com/problems/invert-binary-tree/" },
  { "id": 28, "title": "Maximum Depth of Binary Tree", "difficulty": "Easy", "topic": "Trees", "link": "https://leetcode.com/problems/maximum-depth-of-binary-tree/" },
  { "id": 29, "title": "Diameter of Binary Tree", "difficulty": "Easy", "topic": "Trees", "link": "https://leetcode.com/problems/diameter-of-binary-tree/" },
  { "id": 30, "title": "Balanced Binary Tree", "difficulty": "Easy", "topic": "Trees", "link": "https://leetcode.com/problems/balanced-binary-tree/" },
  { "id": 31, "title": "Same Tree", "difficulty": "Easy", "topic": "Trees", "link": "https://leetcode.com/problems/same-tree/" },
  { "id": 32, "title": "Subtree of Another Tree", "difficulty": "Easy", "topic": "Trees", "link": "https://leetcode.com/problems/subtree-of-another-tree/" },
  { "id": 33, "title": "Lowest Common Ancestor of a BST", "difficulty": "Medium", "topic": "Trees", "link": "https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-search-tree/" },
  { "id": 34, "title": "Binary Tree Level Order Traversal", "difficulty": "Medium", "topic": "Trees", "link": "https://leetcode.com/problems/binary-tree-level-order-traversal/" },
  { "id": 35, "title": "Validate Binary Search Tree", "difficulty": "Medium", "topic": "Trees", "link": "https://leetcode.com/problems/validate-binary-search-tree/" },
  { "id": 36, "title": "Kth Smallest Element in a BST", "difficulty": "Medium", "topic": "Trees", "link": "https://leetcode.com/problems/kth-smallest-element-in-a-bst/" },
  { "id": 37, "title": "Construct Binary Tree from Preorder and Inorder Traversal", "difficulty": "Medium", "topic": "Trees", "link": "https://leetcode.com/problems/construct-binary-tree-from-preorder-and-inorder-traversal/" },
  { "id": 38, "title": "Binary Tree Maximum Path Sum", "difficulty": "Hard", "topic": "Trees", "link": "https://leetcode.com/problems/binary-tree-maximum-path-sum/" },
  { "id": 39, "title": "Serialize and Deserialize Binary Tree", "difficulty": "Hard", "topic": "Trees", "link": "https://leetcode.com/problems/serialize-and-deserialize-binary-tree/" },
  { "id": 58, "title": "Binary Tree Right Side View", "difficulty": "Medium", "topic": "Trees", "link": "https://leetcode.com/problems/binary-tree-right-side-view/" },
  
  # Tries
  { "id": 40, "title": "Implement Trie (Prefix Tree)", "difficulty": "Medium", "topic": "Tries", "link": "https://leetcode.com/problems/implement-trie-prefix-tree/" },
  { "id": 41, "title": "Design Add and Search Words Data Structure", "difficulty": "Medium", "topic": "Tries", "link": "https://leetcode.com/problems/design-add-and-search-words-data-structure/" },
  
  # Heap / Priority Queue
  { "id": 42, "title": "Find Median from Data Stream", "difficulty": "Hard", "topic": "Heap", "link": "https://leetcode.com/problems/find-median-from-data-stream/" },
  { "id": 67, "title": "K Closest Points to Origin", "difficulty": "Medium", "topic": "Heap", "link": "https://leetcode.com/problems/k-closest-points-to-origin/" },
  { "id": 68, "title": "Kth Largest Element in an Array", "difficulty": "Medium", "topic": "Heap", "link": "https://leetcode.com/problems/kth-largest-element-in-an-array/" },
  { "id": 69, "title": "Task Scheduler", "difficulty": "Medium", "topic": "Heap", "link": "https://leetcode.com/problems/task-scheduler/" },

  # Backtracking
  { "id": 43, "title": "Combination Sum", "difficulty": "Medium", "topic": "Backtracking", "link": "https://leetcode.com/problems/combination-sum/" },
  { "id": 44, "title": "Permutations", "difficulty": "Medium", "topic": "Backtracking", "link": "https://leetcode.com/problems/permutations/" },
  { "id": 59, "title": "Subsets", "difficulty": "Medium", "topic": "Backtracking", "link": "https://leetcode.com/problems/subsets/" },
  { "id": 60, "title": "Word Search", "difficulty": "Medium", "topic": "Backtracking", "link": "https://leetcode.com/problems/word-search/" },
  { "id": 76, "title": "Letter Combinations of a Phone Number", "difficulty": "Medium", "topic": "Backtracking", "link": "https://leetcode.com/problems/letter-combinations-of-a-phone-number/" },

  # Graphs
  { "id": 45, "title": "Number of Islands", "difficulty": "Medium", "topic": "Graphs", "link": "https://leetcode.com/problems/number-of-islands/" },
  { "id": 46, "title": "Clone Graph", "difficulty": "Medium", "topic": "Graphs", "link": "https://leetcode.com/problems/clone-graph/" },
  { "id": 47, "title": "Pacific Atlantic Water Flow", "difficulty": "Medium", "topic": "Graphs", "link": "https://leetcode.com/problems/pacific-atlantic-water-flow/" },
  { "id": 48, "title": "Course Schedule", "difficulty": "Medium", "topic": "Graphs", "link": "https://leetcode.com/problems/course-schedule/" },
  { "id": 70, "title": "Rotting Oranges", "difficulty": "Medium", "topic": "Graphs", "link": "https://leetcode.com/problems/rotting-oranges/" },
  { "id": 71, "title": "Redundant Connection", "difficulty": "Medium", "topic": "Graphs", "link": "https://leetcode.com/problems/redundant-connection/" },
  { "id": 72, "title": "Word Ladder", "difficulty": "Hard", "topic": "Graphs", "link": "https://leetcode.com/problems/word-ladder/" },

  # 1D DP
  { "id": 49, "title": "Climbing Stairs", "difficulty": "Easy", "topic": "Dynamic Programming", "link": "https://leetcode.com/problems/climbing-stairs/" },
  { "id": 50, "title": "House Robber", "difficulty": "Medium", "topic": "Dynamic Programming", "link": "https://leetcode.com/problems/house-robber/" },
  { "id": 51, "title": "Word Break", "difficulty": "Medium", "topic": "Dynamic Programming", "link": "https://leetcode.com/problems/word-break/" },
  { "id": 52, "title": "Longest Increasing Subsequence", "difficulty": "Medium", "topic": "Dynamic Programming", "link": "https://leetcode.com/problems/longest-increasing-subsequence/" },
  { "id": 73, "title": "Coin Change", "difficulty": "Medium", "topic": "Dynamic Programming", "link": "https://leetcode.com/problems/coin-change/" },
  { "id": 74, "title": "Maximum Product Subarray", "difficulty": "Medium", "topic": "Dynamic Programming", "link": "https://leetcode.com/problems/maximum-product-subarray/" },
  { "id": 77, "title": "Palindromic Substrings", "difficulty": "Medium", "topic": "Dynamic Programming", "link": "https://leetcode.com/problems/palindromic-substrings/" },
  { "id": 78, "title": "Decode Ways", "difficulty": "Medium", "topic": "Dynamic Programming", "link": "https://leetcode.com/problems/decode-ways/" },

  # Intervals
  { "id": 53, "title": "Insert Interval", "difficulty": "Medium", "topic": "Intervals", "link": "https://leetcode.com/problems/insert-interval/" },
  { "id": 54, "title": "Merge Intervals", "difficulty": "Medium", "topic": "Intervals", "link": "https://leetcode.com/problems/merge-intervals/" },
  { "id": 55, "title": "Non-overlapping Intervals", "difficulty": "Medium", "topic": "Intervals", "link": "https://leetcode.com/problems/non-overlapping-intervals/" },
  
  # Math & Geometry
  { "id": 79, "title": "Rotate Image", "difficulty": "Medium", "topic": "Math & Geometry", "link": "https://leetcode.com/problems/rotate-image/" },
  { "id": 80, "title": "Spiral Matrix", "difficulty": "Medium", "topic": "Math & Geometry", "link": "https://leetcode.com/problems/spiral-matrix/" },
  { "id": 81, "title": "Set Matrix Zeroes", "difficulty": "Medium", "topic": "Math & Geometry", "link": "https://leetcode.com/problems/set-matrix-zeroes/" },
]

DATA_FILE = "grind75_progress.json"

# --- PERSISTENCE LOGIC ---
def load_data():
    saved_data = []
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r') as f:
                saved_data = json.load(f)
        except Exception:
            pass
    
    saved_dict = {p['id']: p for p in saved_data}
    final_data = []
    for p in INITIAL_PROBLEMS:
        if p['id'] in saved_dict:
            problem = saved_dict[p['id']]
            if 'history' not in problem: problem['history'] = []
            if 'notes' not in problem: problem['notes'] = ""
            final_data.append(problem)
        else:
            new_p = p.copy()
            new_p.update({
                'status': 'New',
                'nextReview': None,
                'interval': 0,
                'history': [],
                'notes': ""
            })
            final_data.append(new_p)
    return final_data

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def calculate_streak(problems):
    activity_dates = set()
    for p in problems:
        for h in p.get('history', []):
            if 'date' in h:
                activity_dates.add(h['date'][:10])
    
    if not activity_dates: return 0

    streak = 0
    today = datetime.now().date()
    check_date = today
    
    if check_date.isoformat() not in activity_dates:
        if (check_date - timedelta(days=1)).isoformat() not in activity_dates:
            return 0
        else:
            check_date -= timedelta(days=1)
            
    while check_date.isoformat() in activity_dates:
        streak += 1
        check_date -= timedelta(days=1)
    return streak

def update_problem_status(problem, quality):
    now = datetime.now()
    new_interval = 1
    new_status = 'Learning'
    
    if quality == 'Fail':
        new_interval = 1
        new_status = 'Learning'
    elif quality == 'Hard':
        new_interval = 3
        new_status = 'Learning'
    elif quality == 'Easy':
        current_int = problem.get('interval', 0)
        new_interval = 7 if current_int == 0 else int(current_int * 2)
        new_status = 'Mastered' if new_interval > 30 else 'Learning'
            
    next_date = (now + timedelta(days=new_interval)).replace(hour=4, minute=0, second=0, microsecond=0)
    
    problem['status'] = new_status
    problem['interval'] = new_interval
    problem['nextReview'] = next_date.isoformat()
    
    if 'history' not in problem: problem['history'] = []
    problem['history'].append({
        'date': now.isoformat(),
        'quality': quality
    })
    
    return problem

def update_note_callback(problem_id, widget_key):
    """Callback to save notes instantly"""
    for p in st.session_state.problems:
        if p['id'] == problem_id:
            p['notes'] = st.session_state[widget_key]
            save_data(st.session_state.problems)
            break

# --- APP LOGIC ---

if 'problems' not in st.session_state:
    st.session_state.problems = load_data()

problems = st.session_state.problems
streak = calculate_streak(problems)

now = datetime.now()
due_problems = []
for p in problems:
    if p['status'] != 'New' and p['nextReview']:
        if datetime.fromisoformat(p['nextReview']) <= now:
            due_problems.append(p)
due_problems.sort(key=lambda x: x['nextReview'])

stats = {"Mastered": 0, "Learning": 0, "New": 0}
for p in problems:
    stats[p['status']] += 1

# --- UI LAYOUT ---

# SIDEBAR: Timer & Data Management
with st.sidebar:
    st.header("⏱️ Study Timer")
    if 'timer_start' not in st.session_state: st.session_state.timer_start = None
    
    if st.session_state.timer_start is None:
        if st.button("▶️ Start Timer"):
            st.session_state.timer_start = datetime.now()
            st.rerun()
    else:
        elapsed = datetime.now() - st.session_state.timer_start
        seconds = int(elapsed.total_seconds())
        st.markdown(f"""
        <div class="timer-box">
            <h3 style="margin:0;">{seconds//60:02d}:{seconds%60:02d}</h3>
            <small>Running...</small>
        </div>
        """, unsafe_allow_html=True)
        if st.button("⏹️ Stop Timer"):
            st.session_state.timer_start = None
            st.success(f"Session ended. Duration: {seconds//60}m {seconds%60}s")
            time.sleep(2)
            st.rerun()
    
    st.divider()
    
    st.header("💾 Data Management")
    st.info("⚠️ Streamlit Cloud may reset your data on update. Download a backup!")
    
    # DOWNLOAD BACKUP
    json_str = json.dumps(problems, indent=2)
    st.download_button(
        label="📥 Download Backup (JSON)",
        data=json_str,
        file_name="grind75_backup.json",
        mime="application/json"
    )
    
    # RESTORE BACKUP
    uploaded_file = st.file_uploader("📤 Restore from Backup", type=["json"])
    if uploaded_file is not None:
        try:
            restored_data = json.load(uploaded_file)
            if isinstance(restored_data, list) and len(restored_data) > 0:
                if st.button("Confirm Restore"):
                    save_data(restored_data)
                    st.session_state.problems = restored_data
                    st.success("✅ Data restored successfully! Reloading...")
                    time.sleep(1)
                    st.rerun()
        except Exception as e:
            st.error(f"Error restoring file: {e}")

    st.divider()
    if st.button("🗑️ Reset All Progress"):
        if os.path.exists(DATA_FILE): os.remove(DATA_FILE)
        st.session_state.problems = load_data()
        st.rerun()

st.title("Grind 75 Smart Tracker")

# Streak Banner
st.markdown(f"""
<div class="streak-container">
    <h2 style="margin:0; padding:0;">🔥 {streak} Day Streak</h2>
    <p style="margin:0;">Keep solving problems daily to maintain your streak!</p>
</div>
""", unsafe_allow_html=True)

# Stats Cards
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f'<div class="stat-card"><div class="stat-value color-green">{stats["Mastered"]}</div><div class="stat-label">Mastered</div></div>', unsafe_allow_html=True)
with col2:
    st.markdown(f'<div class="stat-card"><div class="stat-value color-yellow">{stats["Learning"]}</div><div class="stat-label">Learning</div></div>', unsafe_allow_html=True)
with col3:
    st.markdown(f'<div class="stat-card"><div class="stat-value color-gray">{stats["New"]}</div><div class="stat-label">New</div></div>', unsafe_allow_html=True)

st.progress(stats['Mastered'] / len(problems))

# TABS
tab1, tab2, tab3 = st.tabs(["Daily Check-in", "All Problems", "Progress & History"])

# --- TAB 1: DAILY CHECK-IN ---
with tab1:
    st.header(f"Due Today ({len(due_problems)})")
    if len(due_problems) == 0:
        st.success("🎉 You're all caught up! Go to 'All Problems' to start something new.")
    else:
        for p in due_problems:
            with st.container():
                st.markdown(f"### [{p['title']}]({p['link']})")
                st.caption(f"**{p['difficulty']}** • {p['topic']} • Interval: {p['interval']} days")
                c1, c2, c3 = st.columns(3)
                if c1.button("🔴 Fail (1d)", key=f"q_fail_{p['id']}"):
                    update_problem_status(p, 'Fail'); save_data(problems); st.rerun()
                if c2.button("🟡 Hard (3d)", key=f"q_hard_{p['id']}"):
                    update_problem_status(p, 'Hard'); save_data(problems); st.rerun()
                if c3.button("🟢 Easy (Double)", key=f"q_easy_{p['id']}"):
                    update_problem_status(p, 'Easy'); save_data(problems); st.rerun()
                
                with st.expander("📝 Notes"):
                    rev_key = f"note_{p['id']}_rev"
                    st.text_area("Notes", value=p.get('notes', ""), key=rev_key, on_change=update_note_callback, args=(p['id'], rev_key))
                st.divider()

# --- TAB 2: ALL PROBLEMS ---
with tab2:
    st.header("All Problems")
    topics = sorted(list(set(p['topic'] for p in problems)))
    c_filter, c_search = st.columns([1, 2])
    selected_topic = c_filter.selectbox("Filter by Topic", ["All"] + topics)
    search_query = c_search.text_input("Search Problems", "")
    
    filtered = []
    for p in problems:
        if selected_topic != "All" and p['topic'] != selected_topic: continue
        if search_query:
            q = search_query.lower()
            if q not in p['title'].lower() and q not in p['topic'].lower() and q not in p['difficulty'].lower(): continue
        filtered.append(p)
    
    if not filtered: st.info("No problems match.")
    else:
        for p in filtered:
            with st.container():
                c1, c2 = st.columns([3, 1])
                with c1:
                    st.markdown(f"**[{p['title']}]({p['link']})**")
                    color = "color-green" if p['status']=='Mastered' else "color-yellow" if p['status']=='Learning' else "color-gray"
                    st.markdown(f"<span style='color:#666'>{p['difficulty']} • {p['topic']} • <span class='{color}' style='font-weight:bold'>{p['status']}</span></span>", unsafe_allow_html=True)
                with c2:
                    b1, b2, b3 = st.columns(3)
                    if b1.button("🔴", key=f"l_f_{p['id']}"): update_problem_status(p, 'Fail'); save_data(problems); st.rerun()
                    if b2.button("🟡", key=f"l_h_{p['id']}"): update_problem_status(p, 'Hard'); save_data(problems); st.rerun()
                    if b3.button("🟢", key=f"l_e_{p['id']}"): update_problem_status(p, 'Easy'); save_data(problems); st.rerun()
                
                with st.expander("📝 Notes"):
                    norm_key = f"note_{p['id']}"
                    st.text_area("Write notes:", value=p.get('notes', ""), key=norm_key, on_change=update_note_callback, args=(p['id'], norm_key))
                st.divider()

# --- TAB 3: PROGRESS & HISTORY ---
with tab3:
    st.header("📚 Solved Problems & History")
    
    completed = [p for p in problems if p['status'] != 'New']
    
    if not completed:
        st.info("No problems solved yet. Start grinding!")
    else:
        # Prepare Data for Table
        table_data = []
        for p in completed:
            next_review = p['nextReview'][:10] if p['nextReview'] else "N/A"
            stage_desc = f"{p['status']} ({p['interval']}d interval)"
            table_data.append({
                "Problem": p['title'],
                "Topic": p['topic'],
                "Difficulty": p['difficulty'],
                "Stage": stage_desc,
                "Next Review": next_review
            })
        
        df = pd.DataFrame(table_data)
        st.dataframe(
            df, 
            use_container_width=True,
            column_config={
                "Next Review": st.column_config.DateColumn("Next Review", format="YYYY-MM-DD"),
            }
        )