import pandas as pd
import sys

def main():
    if len(sys.argv) != 3:
        print("Usage: python add_user_id.py <input_file.csv> <output_file.csv>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    try:
        df = pd.read_csv(input_file)
        df.insert(0, 'user_id', range(1, len(df) + 1))
        df.to_csv(output_file, index=False)
        print(f"✅ Success: '{output_file}' created with user_id column.")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()

