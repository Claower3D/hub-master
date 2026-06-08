import os

for filename in ["candidate_hubmaster_0.html", "candidate_hubmaster_1.html"]:
    if os.path.exists(filename):
        print(f"=== {filename} ===")
        with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        # Let's count occurences of some key components
        for term in ["initDashboard", "initHeroTimeline", "masters-row", "slider", "review-card", "cabinet"]:
            count = content.lower().count(term.lower())
            print(f"  Term '{term}': found {count} times")
            
        # Let's search for "Total Lines" or typical lines that might show log structures
        log_patterns = ["step_index", "type", "created_at", "source"]
        found_patterns = [p for p in log_patterns if p in content]
        print(f"  Log patterns present: {found_patterns}")
        
        # Print a sample from line 100 to 150
        lines = content.splitlines()
        if len(lines) > 150:
            print("  Lines 100-140:")
            for idx in range(100, 140):
                if idx < len(lines):
                    print(f"    {idx+1}: {lines[idx][:100]}")
        print("="*40)
