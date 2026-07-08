import pandas as pd

from pharma_ai.builders.company_builder import CompanyBuilder

test_df = pd.DataFrame({
    "Company_Name": [
        "Sun Pharma",
        "SUN PHARMA",
        "Zydus Lifesciences",
        "",
        None
    ]
})

builder = CompanyBuilder()

result = builder.run(test_df)

print(result)