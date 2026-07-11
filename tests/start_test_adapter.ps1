$python = "E:\Neo-mofox-instance\bot-3693525299\neo-mofox\.venv\Scripts\python.exe"
Set-Location "E:\plugins\onebot_expand"
& $python -i -c "from tests import call_napcat, is_available; print('TestAdapter ready'); print('NapCat available:', is_available())"
