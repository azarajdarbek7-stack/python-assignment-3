import json

class ResultSaver:

    @staticmethod
    def save_to_json(result):
        try:
            data = {
                "analysis": "Country Analysis",
                "total_students": result["total_students"],
                "total_countries": result["total_countries"],
                "top_3_countries": result["top_3"],
                "all_countries": result["all_countries"]
            }

            with open("output/result.json", "w", encoding="utf-8") as file:
                json.dump(data, file, indent=4)

            print("Result saved to output/result.json")

        except Exception as e:
            print("Error saving file:", e)