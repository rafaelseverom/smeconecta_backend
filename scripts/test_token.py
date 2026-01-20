import sys, os
sys.path.append(os.getcwd())
from app.core.security import criar_token
print(criar_token({'sub':'test@example.com'}))
