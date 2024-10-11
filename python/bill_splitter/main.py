import random


def main():
	"""STAGE 1: INVITE YOUR FRIENDS"""
	number_of_people = input("Enter the number of friends joining (including you): ")
	number_of_people_int = int(number_of_people)

	if number_of_people_int <= 0:
		print("No one is joining for the party")
	else:
		friends = {}
		for i in range(number_of_people_int):
			name = input("Enter the name of every friend (including you), each on a new line: ")
			friends[name] = 0

		print(number_of_people_int)

		"""STAGE 2: SPLIT THE BILL"""
		bill_value = input("Enter the total bill value: ")
		bill_value = int(bill_value)

		lucky = input('Do you want to use the "Who is lucky?" feature? Write Yes/No: ')
		if lucky.lower() == "yes":
			is_lucky = True
			name = random.choice(list(friends.items()))[0]
			print(f"{name} is the lucky one!")
		else:
			is_lucky = False
			print("No one is going to be lucky")

		if is_lucky:
			number_of_people_int -= 1

		amount_per_person = round(bill_value / number_of_people_int, 2)
		for person in friends:
			if is_lucky and person == name:
				continue
			else:
				friends[person] = amount_per_person

		print(friends)

		"""STAGE 3: THE LUCKY ONE"""
		

if __name__ == "__main__":
	main()
