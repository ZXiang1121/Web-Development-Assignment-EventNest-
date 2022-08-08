class Question:
    count_id = 0

    def __init__(self, name, gender, email, subject, remarks, answers):
        Question.count_id +=1
        self.__qn_id = Question.count_id
        self.__name = name
        self.__email = email
        self.__gender = gender
        self.__subject = subject
        self.__remarks = remarks
        self.__answers = answers


    def get_qn_id(self):
        return self.__qn_id

    def get_name(self):
        return self.__name


    def get_gender(self):
        return self.__gender
    
    def get_subject(self):
        return self.__subject

    def get_email(self):
        return self.__email

    def get_remarks(self):
        return self.__remarks
    
    def get_answers(self):
        return self.__answers
    
    

    def set_qn_id(self, qn_id):
        self.__qn_id = qn_id

    def set_name(self, name):
        self.__name = name
        
    def set_email(self, email):
        self.__email = email
        
    def set_gender(self, gender):
        self.__gender = gender
        
    def set_subject(self, subject):
        self.__subject = subject

    def set_remarks(self, remarks):
        self.__remarks = remarks
        
    def set_answers(self, answers):
        self.__answers = answers