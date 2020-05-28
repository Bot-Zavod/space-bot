# проверка имени
def name_check(name):
    try:
        a1, a2 = name.split()
    except ValueError:
        return False
    if len(name) >= 2 and a1.isalpha() and a2.isalpha():
        return True
    else:
        return False


# проверка адреса электронной почты юзера
def email_check(email):
    if email.count(".") + email.count("@") >= 2:
        return True
    else:
        return False


# идея - юзер со стартапом должен расписать свою идею хотя бы в несолько предложений 
def idea_check(idea):
    if idea.count(" ") >= 1 and len(idea) > 7:
        return True
    else:
        return False


# прототип продукта - стартапер пишет хотя бы два слова о прототипе
def prototype_check(prototype):
    if len(prototype) >= 5:
        return True
    else:
        return False


# зачем вам наша акселерационная программа - стартапер пишет хотя бы одно предложение о том зачем именно ему эта программа
# wdynp is why do you need program
def wdynp_check(wdynp):
    if wdynp.count(" ") >= 1 and len(wdynp) > 7:
        return True
    else:
        return False


# компетенции - юзер который хочет стать ментором пишет какие у него компетенции, 
# тип что он умеет. Думаю там хватит того, чтобы было хотя бы два слова
def expertise_check(competencies):
    if competencies.count(" ") >= 1:
        return True
    else:
        return False


# опыт - ментор пишет о своем опыте, хотя бы два слова чтобы было
def experience_check(skill):
    if skill.count(" ") >= 1:
        return True
    else:
        return False


# сайт, или LinkedIn - тут не должно быть меньше трех букв
def site_check(site):
    if len(site) >= 3:
        return True
    else:
        return False

# название организации - партнер пишет название. Не думаю что есть организации состоящие из одной буквы
def name_organisation_check(name):
    if len(name) >= 2:
        return True
    else:
        return False

# Его позиция в этой организации - ну хотя бы чтобы две буквы были что-ли
def position_check(position):
    if len(position) >= 2:
        return True
    else:
        return False

 

