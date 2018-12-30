while True:
    try:
        user_input = int(input("Enter something: \n>> "))
        break
    except ValueError:
        print("Please Enter a number: ")
    except Exception:
        print("Something went wrong")

print("hello world")

