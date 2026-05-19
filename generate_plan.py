#!/usr/bin/env python3
"""
Microsoft Interview Prep - Daily LeetCode Study Plan Generator
Categorizes problems by pattern, ranks by importance, and creates a daily plan.
"""

import csv
import math
from collections import defaultdict

# ──────────────────────────────────────────────────────────────
# PATTERN CLASSIFICATION MAP
# Each LeetCode ID → primary pattern/concept
# ──────────────────────────────────────────────────────────────

PATTERN_MAP = {
    # ── Arrays & Hashing ──
    1: "Arrays & Hashing",
    49: "Arrays & Hashing",
    217: "Arrays & Hashing",
    242: "Arrays & Hashing",
    238: "Arrays & Hashing",
    128: "Arrays & Hashing",
    347: "Arrays & Hashing",
    560: "Arrays & Hashing",
    169: "Arrays & Hashing",
    229: "Arrays & Hashing",
    268: "Arrays & Hashing",
    287: "Arrays & Hashing",
    442: "Arrays & Hashing",
    448: "Arrays & Hashing",
    136: "Arrays & Hashing",
    387: "Arrays & Hashing",
    349: "Arrays & Hashing",
    350: "Arrays & Hashing",
    299: "Arrays & Hashing",
    205: "Arrays & Hashing",
    290: "Arrays & Hashing",
    219: "Arrays & Hashing",
    383: "Arrays & Hashing",
    525: "Arrays & Hashing",
    523: "Arrays & Hashing",
    325: "Arrays & Hashing",
    412: "Arrays & Hashing",
    819: "Arrays & Hashing",
    929: "Arrays & Hashing",
    1470: "Arrays & Hashing",
    1528: "Arrays & Hashing",
    1122: "Arrays & Hashing",
    905: "Arrays & Hashing",
    832: "Arrays & Hashing",
    867: "Arrays & Hashing",
    977: "Arrays & Hashing",
    1304: "Arrays & Hashing",
    1394: "Arrays & Hashing",
    609: "Arrays & Hashing",
    532: "Arrays & Hashing",
    1375: "Arrays & Hashing",

    # ── Two Pointers ──
    15: "Two Pointers",
    11: "Two Pointers",
    167: "Two Pointers",
    125: "Two Pointers",
    16: "Two Pointers",
    18: "Two Pointers",
    75: "Two Pointers",
    283: "Two Pointers",
    26: "Two Pointers",
    27: "Two Pointers",
    344: "Two Pointers",
    680: "Two Pointers",
    611: "Two Pointers",
    88: "Two Pointers",
    844: "Two Pointers",
    28: "Two Pointers",

    # ── Sliding Window ──
    3: "Sliding Window",
    76: "Sliding Window",
    438: "Sliding Window",
    567: "Sliding Window",
    239: "Sliding Window",
    159: "Sliding Window",
    340: "Sliding Window",
    209: "Sliding Window",
    643: "Sliding Window",
    480: "Sliding Window",
    1004: "Sliding Window",
    727: "Sliding Window",
    346: "Sliding Window",
    845: "Sliding Window",
    30: "Sliding Window",
    1156: "Sliding Window",

    # ── Stack ──
    20: "Stack",
    155: "Stack",
    150: "Stack",
    224: "Stack",
    227: "Stack",
    772: "Stack",
    71: "Stack",
    394: "Stack",
    84: "Stack",
    85: "Stack",
    32: "Stack",
    735: "Stack",
    739: "Stack",
    503: "Stack",
    496: "Stack",
    402: "Stack",
    316: "Stack",
    636: "Stack",
    907: "Stack",
    895: "Stack",
    1381: "Stack",
    716: "Stack",
    232: "Stack",
    225: "Stack",
    591: "Stack",
    901: "Stack",
    1249: "Stack",

    # ── Binary Search ──
    33: "Binary Search",
    153: "Binary Search",
    162: "Binary Search",
    74: "Binary Search",
    81: "Binary Search",
    34: "Binary Search",
    240: "Binary Search",
    540: "Binary Search",
    702: "Binary Search",
    278: "Binary Search",
    69: "Binary Search",
    367: "Binary Search",
    704: "Binary Search",
    852: "Binary Search",
    658: "Binary Search",
    35: "Binary Search",
    378: "Binary Search",
    1539: "Binary Search",

    # ── Linked List ──
    138: "Linked List",
    2: "Linked List",
    206: "Linked List",
    21: "Linked List",
    25: "Linked List",
    445: "Linked List",
    143: "Linked List",
    141: "Linked List",
    142: "Linked List",
    160: "Linked List",
    19: "Linked List",
    234: "Linked List",
    328: "Linked List",
    148: "Linked List",
    92: "Linked List",
    61: "Linked List",
    82: "Linked List",
    83: "Linked List",
    86: "Linked List",
    237: "Linked List",
    876: "Linked List",
    147: "Linked List",
    203: "Linked List",
    707: "Linked List",
    708: "Linked List",
    430: "Linked List",
    1019: "Linked List",
    1474: "Linked List",

    # ── Trees (BFS/DFS) ──
    102: "Trees",
    103: "Trees",
    107: "Trees",
    199: "Trees",
    98: "Trees",
    236: "Trees",
    235: "Trees",
    105: "Trees",
    106: "Trees",
    116: "Trees",
    117: "Trees",
    297: "Trees",
    428: "Trees",
    449: "Trees",
    431: "Trees",
    545: "Trees",
    114: "Trees",
    110: "Trees",
    226: "Trees",
    101: "Trees",
    104: "Trees",
    111: "Trees",
    100: "Trees",
    572: "Trees",
    543: "Trees",
    124: "Trees",
    112: "Trees",
    113: "Trees",
    257: "Trees",
    230: "Trees",
    270: "Trees",
    285: "Trees",
    510: "Trees",
    450: "Trees",
    701: "Trees",
    669: "Trees",
    173: "Trees",
    314: "Trees",
    987: "Trees",
    655: "Trees",
    222: "Trees",
    662: "Trees",
    515: "Trees",
    958: "Trees",
    993: "Trees",
    863: "Trees",
    1008: "Trees",
    938: "Trees",
    872: "Trees",
    671: "Trees",
    652: "Trees",
    333: "Trees",
    129: "Trees",
    437: "Trees",
    426: "Trees",
    108: "Trees",
    109: "Trees",
    99: "Trees",
    144: "Trees",
    94: "Trees",
    341: "Trees",
    1145: "Trees",
    979: "Trees",
    513: "Trees",
    654: "Trees",
    1038: "Trees",
    1339: "Trees",
    1448: "Trees",
    1469: "Trees",
    1273: "Trees",

    # ── Tries ──
    208: "Trie",
    212: "Trie",
    211: "Trie",
    642: "Trie",
    676: "Trie",
    472: "Trie",
    1062: "Trie",

    # ── Heap / Priority Queue ──
    23: "Heap",
    295: "Heap",
    215: "Heap",
    973: "Heap",
    692: "Heap",
    703: "Heap",
    373: "Heap",
    632: "Heap",
    358: "Heap",
    767: "Heap",
    621: "Heap",
    253: "Heap",
    407: "Heap",
    630: "Heap",

    # ── Backtracking ──
    46: "Backtracking",
    47: "Backtracking",
    78: "Backtracking",
    90: "Backtracking",
    77: "Backtracking",
    39: "Backtracking",
    40: "Backtracking",
    216: "Backtracking",
    22: "Backtracking",
    17: "Backtracking",
    51: "Backtracking",
    37: "Backtracking",
    79: "Backtracking",
    93: "Backtracking",
    131: "Backtracking",
    267: "Backtracking",
    784: "Backtracking",
    1079: "Backtracking",
    60: "Backtracking",
    282: "Backtracking",
    489: "Backtracking",
    351: "Backtracking",

    # ── Graph ──
    200: "Graph",
    133: "Graph",
    207: "Graph",
    210: "Graph",
    269: "Graph",
    127: "Graph",
    126: "Graph",
    547: "Graph",
    695: "Graph",
    694: "Graph",
    286: "Graph",
    417: "Graph",
    323: "Graph",
    305: "Graph",
    721: "Graph",
    332: "Graph",
    785: "Graph",
    399: "Graph",
    733: "Graph",
    994: "Graph",
    490: "Graph",
    934: "Graph",
    909: "Graph",
    1091: "Graph",
    1192: "Graph",
    886: "Graph",
    743: "Graph",
    787: "Graph",
    1197: "Graph",
    317: "Graph",
    529: "Graph",

    # ── Dynamic Programming ──
    5: "Dynamic Programming",
    10: "Dynamic Programming",
    44: "Dynamic Programming",
    42: "Dynamic Programming",
    53: "Dynamic Programming",
    70: "Dynamic Programming",
    121: "Dynamic Programming",
    122: "Dynamic Programming",
    123: "Dynamic Programming",
    139: "Dynamic Programming",
    140: "Dynamic Programming",
    91: "Dynamic Programming",
    152: "Dynamic Programming",
    198: "Dynamic Programming",
    213: "Dynamic Programming",
    300: "Dynamic Programming",
    322: "Dynamic Programming",
    518: "Dynamic Programming",
    62: "Dynamic Programming",
    63: "Dynamic Programming",
    64: "Dynamic Programming",
    72: "Dynamic Programming",
    97: "Dynamic Programming",
    120: "Dynamic Programming",
    174: "Dynamic Programming",
    221: "Dynamic Programming",
    279: "Dynamic Programming",
    304: "Dynamic Programming",
    354: "Dynamic Programming",
    403: "Dynamic Programming",
    416: "Dynamic Programming",
    494: "Dynamic Programming",
    516: "Dynamic Programming",
    651: "Dynamic Programming",
    688: "Dynamic Programming",
    887: "Dynamic Programming",
    935: "Dynamic Programming",
    1027: "Dynamic Programming",
    1143: "Dynamic Programming",
    1155: "Dynamic Programming",
    1246: "Dynamic Programming",
    805: "Dynamic Programming",
    568: "Dynamic Programming",
    45: "Dynamic Programming",
    55: "Dynamic Programming",
    134: "Dynamic Programming",
    1458: "Dynamic Programming",
    1510: "Dynamic Programming",
    650: "Dynamic Programming",
    698: "Dynamic Programming",
    329: "Dynamic Programming",
    413: "Dynamic Programming",
    1092: "Dynamic Programming",

    # ── Greedy ──
    135: "Greedy",
    435: "Greedy",
    452: "Greedy",
    406: "Greedy",
    280: "Greedy",
    670: "Greedy",

    # ── Intervals ──
    56: "Intervals",
    57: "Intervals",
    252: "Intervals",
    228: "Intervals",
    759: "Intervals",
    729: "Intervals",
    1229: "Intervals",
    1386: "Intervals",

    # ── Math & Bit Manipulation ──
    7: "Math",
    9: "Math",
    12: "Math",
    13: "Math",
    29: "Math",
    43: "Math",
    50: "Math",
    168: "Math",
    171: "Math",
    172: "Math",
    191: "Math",
    204: "Math",
    231: "Math",
    258: "Math",
    338: "Math",
    397: "Math",
    405: "Math",
    470: "Math",
    509: "Math",
    1185: "Math",
    1344: "Math",
    1523: "Math",
    1518: "Math",
    674: "Math",
    679: "Math",

    # ── String Manipulation ──
    8: "String",
    273: "String",
    165: "String",
    443: "String",
    6: "String",
    14: "String",
    151: "String",
    186: "String",
    557: "String",
    535: "String",
    722: "String",
    468: "String",
    65: "String",
    38: "String",
    796: "String",
    917: "String",
    541: "String",
    556: "String",
    564: "String",
    166: "String",
    459: "String",
    884: "String",
    953: "String",
    833: "String",
    1324: "String",
    1417: "String",
    1415: "String",

    # ── Matrix ──
    54: "Matrix",
    48: "Matrix",
    73: "Matrix",
    59: "Matrix",
    289: "Matrix",
    36: "Matrix",
    498: "Matrix",
    419: "Matrix",
    463: "Matrix",
    939: "Matrix",
    1013: "Matrix",

    # ── Design ──
    146: "Design",
    348: "Design",
    277: "Design",
    380: "Design",
    381: "Design",
    460: "Design",
    706: "Design",
    622: "Design",
    362: "Design",
    379: "Design",
    384: "Design",
    432: "Design",
    528: "Design",
    981: "Design",
    1188: "Design",
    1206: "Design",
    631: "Design",

    # ── Divide & Conquer ──
    4: "Divide & Conquer",
    218: "Divide & Conquer",
    315: "Divide & Conquer",
    493: "Divide & Conquer",
    327: "Divide & Conquer",  # actually this isn't in the list but keeping for safety

    # ── Union Find ──
    684: "Union Find",  # not in list but keep for pattern coverage

    # ── Bit Manipulation ──
    89: "Bit Manipulation",
    187: "Bit Manipulation",
    220: "Bit Manipulation",
    1371: "Bit Manipulation",
    1318: "Bit Manipulation",

    # ── Sorting ──
    179: "Sorting",
    969: "Sorting",
    950: "Sorting",
    31: "Sorting",
    1053: "Sorting",

    # ── Binary Search on Answer / Special ──
    1044: "Binary Search",
    308: "Binary Search",

    # ── Game Theory / Simulation ──
    794: "Simulation",
    289: "Simulation",
    575: "Math",

    # ── Miscellaneous / Multi-pattern ──
    223: "Math",
    836: "Math",
    365: "Math",
    176: "SQL",
    612: "SQL",
    1285: "SQL",
    1369: "SQL",

    # ── Concurrency ──
    1114: "Concurrency",
    1116: "Concurrency",

    # ── Graph (BFS special) ──
    773: "Graph",
    843: "Graph",
    1236: "Graph",
    1306: "Graph",

    # ── DFS on arrays / special backtracking ──
    419: "Matrix",
    457: "Two Pointers",

    # ── Misc remaining ──
    828: "String",
    1131: "Math",
    1093: "Math",
    1198: "Binary Search",
    972: "Math",
    1006: "Math",
    871: "Greedy",
    788: "Math",
    281: "Design",
}

# ──────────────────────────────────────────────────────────────
# DIFFICULTY TIERS FOR IMPORTANCE WEIGHTING
# ──────────────────────────────────────────────────────────────

DIFFICULTY_WEIGHT = {
    "Easy": 1.0,
    "Medium": 1.5,
    "Hard": 2.0,
}

def load_problems(filepath):
    """Load problems from CSV and compute importance score."""
    problems = []
    with open(filepath, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            pid = int(row["ID"].strip())
            title = row["Title"].strip()
            acceptance = row["Acceptance"].strip().replace("%", "")
            difficulty = row["Difficulty"].strip()
            frequency = float(row["Frequency"].strip())
            link = row["Leetcode Question Link"].strip()

            pattern = PATTERN_MAP.get(pid, "Uncategorized")

            # Importance score: frequency is the primary driver
            # Bonus for Medium/Hard since they test deeper understanding
            diff_w = DIFFICULTY_WEIGHT.get(difficulty, 1.0)
            importance = frequency * diff_w

            problems.append({
                "id": pid,
                "title": title,
                "acceptance": acceptance,
                "difficulty": difficulty,
                "frequency": frequency,
                "link": link,
                "pattern": pattern,
                "importance": importance,
            })
    return problems


def select_top_problems(problems, max_per_pattern=None):
    """
    Select top problems sorted by importance.
    Filter out SQL/Concurrency (not relevant for coding rounds).
    Keep problems with frequency > 0 first, then fill with 0-freq if needed.
    """
    # Filter out non-coding patterns
    skip_patterns = {"SQL", "Concurrency", "Uncategorized"}
    filtered = [p for p in problems if p["pattern"] not in skip_patterns]

    # Split into high-freq and zero-freq
    high_freq = sorted([p for p in filtered if p["frequency"] > 0],
                       key=lambda x: x["importance"], reverse=True)
    zero_freq = sorted([p for p in filtered if p["frequency"] == 0],
                       key=lambda x: x["id"])

    return high_freq, zero_freq


def build_daily_plan(high_freq_problems, zero_freq_problems, problems_per_day=5):
    """
    Build a daily study plan ensuring each day has diverse patterns.
    Strategy:
    - Group problems by pattern
    - For each day, pick one problem from different patterns
    - Prioritize higher importance problems first
    - Mix difficulties: aim for 1 Easy + 2-3 Medium + 1 Hard per day
    """
    # Group by pattern, sorted by importance within each group
    pattern_queues = defaultdict(list)
    for p in high_freq_problems:
        pattern_queues[p["pattern"]].append(p)

    # Also add zero_freq problems at the end of their pattern queues
    for p in zero_freq_problems:
        pattern_queues[p["pattern"]].append(p)

    # Sort each pattern queue by importance (descending)
    for pat in pattern_queues:
        pattern_queues[pat].sort(key=lambda x: x["importance"], reverse=True)

    # Calculate total problems
    total = sum(len(q) for q in pattern_queues.values())
    total_days = math.ceil(total / problems_per_day)

    # Pattern priority: rotate through patterns sorted by their total importance
    pattern_order = sorted(
        pattern_queues.keys(),
        key=lambda p: sum(x["importance"] for x in pattern_queues[p]),
        reverse=True
    )

    days = []
    used_ids = set()
    pattern_idx = 0

    for day_num in range(1, total_days + 1):
        day_problems = []
        day_patterns_used = set()
        attempts = 0

        while len(day_problems) < problems_per_day and attempts < len(pattern_order) * 2:
            pat = pattern_order[pattern_idx % len(pattern_order)]
            pattern_idx += 1
            attempts += 1

            if pat in day_patterns_used:
                continue

            # Find next available problem from this pattern
            while pattern_queues[pat] and pattern_queues[pat][0]["id"] in used_ids:
                pattern_queues[pat].pop(0)

            if pattern_queues[pat]:
                prob = pattern_queues[pat].pop(0)
                used_ids.add(prob["id"])
                day_problems.append(prob)
                day_patterns_used.add(pat)

        if day_problems:
            # Sort within day: Easy → Medium → Hard
            diff_order = {"Easy": 0, "Medium": 1, "Hard": 2}
            day_problems.sort(key=lambda x: diff_order.get(x["difficulty"], 1))
            days.append(day_problems)

    return days


def generate_csv_for_sheets(days, output_path):
    """Generate a CSV file formatted for Google Sheets import."""
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        # Header
        writer.writerow([
            "Day",
            "Problem #",
            "ID",
            "Title",
            "Difficulty",
            "Pattern",
            "Frequency",
            "Link",
            "Dilshad ✅",
            "Yash ✅"
        ])

        for day_idx, day_problems in enumerate(days, 1):
            for prob_idx, prob in enumerate(day_problems, 1):
                writer.writerow([
                    f"Day {day_idx}",
                    prob_idx,
                    prob["id"],
                    prob["title"],
                    prob["difficulty"],
                    prob["pattern"],
                    f"{prob['frequency']:.2f}",
                    prob["link"],
                    "",  # Dilshad column
                    "",  # Yash column
                ])
            # Add empty separator row between days
            writer.writerow([])

    print(f"✅ CSV exported to: {output_path}")


def print_summary(days, high_freq, zero_freq):
    """Print a summary of the study plan."""
    total_problems = sum(len(d) for d in days)
    total_days = len(days)

    # Count by difficulty
    diff_count = defaultdict(int)
    pattern_count = defaultdict(int)
    for day in days:
        for p in day:
            diff_count[p["difficulty"]] += 1
            pattern_count[p["pattern"]] += 1

    print("\n" + "=" * 60)
    print("📊 MICROSOFT INTERVIEW PREP - STUDY PLAN SUMMARY")
    print("=" * 60)
    print(f"\n📅 Total Days: {total_days}")
    print(f"📝 Total Problems: {total_problems}")
    print(f"   (High-frequency: {len(high_freq)}, Zero-frequency bonus: {len(zero_freq)})")
    print(f"📊 Problems per day: ~{total_problems / total_days:.1f}")

    print(f"\n🎯 Difficulty Breakdown:")
    for diff in ["Easy", "Medium", "Hard"]:
        count = diff_count.get(diff, 0)
        pct = (count / total_problems * 100) if total_problems else 0
        bar = "█" * int(pct / 2)
        print(f"   {diff:8s}: {count:3d} ({pct:5.1f}%) {bar}")

    print(f"\n🧩 Pattern Breakdown:")
    for pat, count in sorted(pattern_count.items(), key=lambda x: -x[1]):
        print(f"   {pat:25s}: {count:3d} problems")

    print(f"\n📋 First 5 Days Preview:")
    for day_idx, day_problems in enumerate(days[:5], 1):
        print(f"\n   ── Day {day_idx} ──")
        for p in day_problems:
            emoji = {"Easy": "🟢", "Medium": "🟡", "Hard": "🔴"}.get(p["difficulty"], "⚪")
            print(f"   {emoji} [{p['pattern']:20s}] #{p['id']:4d} {p['title']}")


def main():
    import os
    base_dir = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(base_dir, "microsoft_alltime.csv")

    print("🔄 Loading problems from CSV...")
    problems = load_problems(filepath)
    print(f"   Loaded {len(problems)} problems.")

    print("🔄 Ranking by importance and filtering...")
    high_freq, zero_freq = select_top_problems(problems)
    print(f"   High-frequency: {len(high_freq)}, Zero-frequency: {len(zero_freq)}")

    print("🔄 Building daily study plan with diverse patterns...")
    days = build_daily_plan(high_freq, zero_freq, problems_per_day=5)

    print_summary(days, high_freq, zero_freq)

    output_csv = os.path.join(base_dir, "microsoft_daily_plan.csv")
    generate_csv_for_sheets(days, output_csv)

    print(f"\n🎉 Done! Import '{output_csv}' into Google Sheets.")
    print("   File → Import → Upload → select the CSV → Replace spreadsheet")


if __name__ == "__main__":
    main()
