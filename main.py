import os
import csv
import json

class FileManager:

    @staticmethod
    def check_files():
        print("Checking file...")

        if not os.path.exists("students.csv"):
            print("Error: students.csv not found. Please download the file from LMS.")
            return False

        print("File found: students.csv")

        print("\nChecking output folder...")
        if not os.path.exists("output"):
            os.makedirs("output")
            print("Output folder created: output/")
        else:
            print("Output folder already exists: output/")

        return True


class DataLoader:

    @staticmethod
    def load_data(filename):
        students = []

        try:
            print("\nLoading data...")
            with open(filename, encoding='utf-8') as f:
                reader = csv.DictReader(f)

                for row in reader:
                    students.append(row)

            print(f"Data loaded successfully: {len(students)} students")
            return students

        except Exception as e:
            print("Error while reading file:", e)
            return []


class DataAnalyser:

    @staticmethod
    def preview_data(students, n=5):
        print(f"\nFirst {n} rows:")
        print("-" * 40)

        for s in students[:n]:
            print(f"{s['student_id']} | {s['age']} | {s['gender']} | {s['country']} | GPA: {s['GPA']}")

        print("-" * 40)

    @staticmethod
    def analyse_countries(students):

        countries = list(map(lambda s: s['country'], students))

        country_counts = {}

        for country in countries:
            if country in country_counts:
                country_counts[country] += 1
            else:
                country_counts[country] = 1

        sorted_countries = sorted(
            country_counts.items(),
            key=lambda x: x[1],
            reverse=True
        )

        top_3 = sorted_countries[:3]
        popular_countries = list(filter(lambda x: x[1] > 800, sorted_countries))
        formatted_output = list(map(lambda x: f"{x[0]} : {x[1]}", sorted_countries))

        print("\nStudents by Country")
        print("-" * 30)
        for line in formatted_output:
            print(line)

        print("\nTop 3 Countries:")
        for i, (country, count) in enumerate(top_3, start=1):
            print(f"{i}. {country} : {count}")

        return {
            "total_students": len(students),
            "total_countries": len(country_counts),
            "top_3": top_3,
            "all_countries": country_counts,
            "popular_countries": popular_countries
        }


class ResultSaver:

    @staticmethod
    def save_to_json(result):
        try:
            output_data = {
                "analysis": "Country Analysis",
                "total_students": result["total_students"],
                "total_countries": result["total_countries"],
                "top_3_countries": [
                    {"country": c, "count": cnt}
                    for c, cnt in result["top_3"]
                ],
                "all_countries": result["all_countries"]
            }

            with open("output/result.json", "w", encoding="utf-8") as f:
                json.dump(output_data, f, indent=4)

            print("\n==============================")
            print("ANALYSIS RESULT")
            print("==============================")
            print(f"Analysis : Country Analysis")
            print(f"Total students : {result['total_students']}")
            print(f"Total countries : {result['total_countries']}")

            print("\nTop 3 Countries:")
            for i, (c, cnt) in enumerate(result["top_3"], start=1):
                print(f"{i}. {c} : {cnt}")

            print("\nResult saved to output/result.json")

        except Exception as e:
            print("Error saving JSON:", e)


def main():
    # Step 1: check files
    if not FileManager.check_files():
        return

    # Step 2: load data
    students = DataLoader.load_data("students.csv")
    if not students:
        return

    DataAnalyser.preview_data(students)

    result = DataAnalyser.analyse_countries(students)

    ResultSaver.save_to_json(result)


if __name__ == "__main__":
    main()