
import helper_func as hf
import general_func as gf

def main():

    #Готовые вспомогательные функции
    print(hf.normalize_input_data('HdfjjweWgnkndsg', '10'))
    hf.submenu()

    #Шаблоны основных функций
    gf.start_menu()
    gf.crypto('string', 3) 
    gf.input_params()
    gf.generating_params()
    gf.result()


if __name__ == '__main__':
    main()
