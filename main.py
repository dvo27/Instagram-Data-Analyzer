import sys
import message as msg
import followers as follow


def main():
    valid_options = ['1', '2', 'Q', 'q']

    menu_choice = input('Please choose an option below!:'
                        '\n[1] : Get DMs With Specific User Data\n'
                        '[2] : Get Follow Data\n'
                        '[Q] : Quit Program\n'
                        '-------------------------------------\n')

    if menu_choice not in valid_options:
        print('\nInvalid option! Please try again.\n')
        main()
    else:
        if menu_choice == '1':
            msg.message_data()
        elif menu_choice == '2':
            follow.follow_data()
        elif menu_choice == 'Q' or 'q':
            print('\nEnding program...Goodbye!')
            sys.exit()


if __name__ == '__main__':
    main()
