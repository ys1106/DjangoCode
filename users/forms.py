from django import forms


# 로그인 폼
class LoginForm(forms.Form):
    userid = forms.CharField( # 아이디
        max_length=50,
        label='아이디',
        widget=forms.TextInput({ # TextInput 위젯 사용하여 입력받을 것
            'placeholder': '아이디를 입력해주세요' # 입력 전 나오는 문구
        })
    )
    password = forms.CharField( # 비밀번호
        max_length=30,
        min_length=5,
        label='비밀번호',
        widget=forms.PasswordInput({ # PasswordInput 위젯 사용하여 입력받을 것
            'placeholder': '비밀번호를 입력해주세요' # 입력 전 나오는 문구
        })
    )

# 회원가입 폼
class SignupForm(forms.Form):
    userid = forms.CharField(# 아이디
        max_length=50,
        label='아이디',
        required=True, #꼭 입력해야하는 값
        help_text = '50자 이하의 문자나 숫자, 그리고 특수문자(@/./+/-/_)만 입력 가능합니다.'
    )
    password1 = forms.CharField( # 비밀번호
        label='비밀번호',
        max_length=30,
        min_length=5,
        required=True, # 꼭 입력해야 하는 값
        strip=False, # 입력값 안 보이게
        widget=forms.PasswordInput, #PasswordInput 위젯 사용
        help_text='5자 이상 30자 이하의 비밀번호를 입력해주세요. 비밀번호는 개인정보와 비슷하거나, 전부 숫자로 할 수 없습니다.'
    )

    password2 = forms.CharField( # 비밀번호 확인
        label='비밀번호 확인',
        required=True,
        strip=False,
        widget=forms.PasswordInput,
        help_text='위에서 입력한 비밀번호와 동일한 비밀번호를 입력해주세요.'
    )

    name = forms.CharField( # 이름
        label='이름',
        max_length=15,
        required=True
    )

    email = forms.EmailField() # 이메일

    birth = forms.DateField( # 생년월일
        label='생년월일',
        required=True,
        widget=forms.DateInput({ # DateInput위젯 이용하여 입력
            'type' : 'date'
        })
    )

    def password_check(self): # 회원가입 시 입력한 두 개의 비밀번호가 일치하는지 확인
        password1 = self.cleaned_data.get("password1") # 처음 입력한 비밀번호
        password2 = self.cleaned_data.get("password2") # 뒤에 입력한 비밀번호
        if password1 and password2 and password1 != password2: # 둘 중 하나라도 값을 입력하지 않았거나 두 값이 다르면
            raise forms.ValidationError( # 에러 발생시킴
                self.error_message['password_mismatch'], # 에러메시지
                code='password+mismatch'
            )
        return password2 # 조건을 모두 만족한 비밀번호 리턴
