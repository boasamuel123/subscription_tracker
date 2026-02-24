import pandas as pd
import matplotlib.pyplot as plt
import time

print("transaction file")
transactions = input("")
df = pd.read_csv(transactions)


#data cleaning

df["merchants"] = (
    df["description"]
    .str.split("/").str[0]
    .str.replace(r"\d+|\.COM|LTD|[^A-Z\s]", "", regex=True)
    .str.strip()
    .str.upper()
)

df = df[df["amount"] < 0]
occur = df["merchants"].value_counts()
occurs = occur[occur > 3 ]
result = (
    df.groupby(["merchants", "amount"])
      .size()
      .reset_index(name="occurrences")
)

result = result[result["occurrences"] > 5]

filtered = df[df["merchants"].isin(occurs.index)]

avg_charge = filtered.groupby("merchants")["amount"].mean()


df2 = pd.concat([occurs, avg_charge], axis=1)

df2.columns = ["occurences", "monthly_cost"]

df2["annual_cost"] = df2["monthly_cost"] * 12

df2 = df2.reset_index()  # moves merchant names into column

df2.columns = ["merchants", "occurences", "monthly_cost", "annual_cost"]
df2["months"] = df["date"]
months = df2.groupby("months")["monthly_cost"].sum()
df2.to_csv("subscriptions_detected.csv")

#matplotlib charts
def barplot():
    plt.figure(figsize=(6,10))
    plt.style.use("dark_background")
    plt.title("top subscriptions chart")
    plt.xlabel("merchants")
    plt.ylabel("estimated monthly cost")
    plt.bar(result["merchants"], result["amount"], color="grey")
    plt.grid(color='white', linestyle='-')
    plt.savefig("top_subscriptions.png")
    plt.show()



#main program
def main():
    running = True

    print("starting....")
    time.sleep(3)

    while running:
     print("========welcome to subscription tracker==========")
     print("1.show subscriptions")
     print("2.show top subscriptions")
     print("3.exit")
     choice = int(input(""))
     if choice == 1:
        print("\nsubscriptions detected:",result)
     elif choice == 2:
        barplot()
     elif choice == 3:
        print("\napplication closing...")
        time.sleep(3)
        running = False

main()



