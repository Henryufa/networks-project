# users = {
#     "Tom" : "Tom11",
#     "David" : "David22",
#     "Beth" : "Beth33"
# }

# with open("users.txt","w") as f:
#     for key, value in users.items():
#         f.write(f"({key}, {value})\n")
import os.path

print(os.path.isfile("users.txt"))
