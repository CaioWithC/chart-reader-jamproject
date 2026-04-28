import sys
import os
import ChartParser
import TimingEngine
import DifficultyCalculator

# =========================
# MAIN (CLI SUPPORT)
# =========================

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python script.py <chart_file.chart>")
        sys.exit(1)

    chart_file = sys.argv[1]

    # get filename without extension
    parser = ChartParser.ChartParser(chart_file)

    notes = parser.parse()
    formatted_title = parser.format_title(parser.title)    
    parser.title = formatted_title    

    output_file = formatted_title + ".txt"

    timing = TimingEngine.TimingEngine(parser.resolution, parser.bpms)

    calc = DifficultyCalculator.DifficultyCalculator(notes, timing, parser.resolution)
    stars, patterns = calc.compute_stars()

    # separar tipos
    hopo_notes, strum_notes = calc.split_note_types()

    # calcular separado
    hopo_stars, hopo_patterns = calc.compute_stars_for_notes(hopo_notes)
    strum_stars, strum_patterns = calc.compute_stars_for_notes(strum_notes)
    
    # console output
    print(f"Title: {parser.title}")
    print(f"Artist: {parser.artist}")
    print(f"\nFile: {chart_file}\n")
    print(f"★ Difficulty: {stars:.2f}/10")
    print("Patterns detected:")
    for k, v in patterns.items():
        print(f"  {k}: {v}")
        
    # write to txt
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(f"Title: {parser.title}\n")
        f.write(f"Artist: {parser.artist}\n")
        f.write(f"File: {chart_file}\n\n")    

        #    =====================
        # ALL NOTES
        # =====================
        f.write("=== OVERALL ===\n")
        f.write(f"Difficulty: {stars:.2f}/10\n")
        f.write("Patterns:\n")
        for k, v in patterns.items():
            f.write(f"{k}: {v}\n")

        # =====================
        # HOPOs
        # =====================
        f.write("\n=== ALL HOPOs ===\n")
        f.write(f"Difficulty: {hopo_stars:.2f}/10\n")
        f.write("Patterns:\n")
        for k, v in hopo_patterns.items():
            f.write(f"{k}: {v}\n")

        # =====================
        # STRUMs
        # =====================
        f.write("\n=== ALL STRUMs ===\n")
        f.write(f"Difficulty: {strum_stars:.2f}/10\n")
        f.write("Patterns:\n")
        for k, v in strum_patterns.items():
            f.write(f"{k}: {v}\n")
        print(f"📄 Results saved to: {formatted_title}")
