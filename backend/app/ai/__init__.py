# FILE:        backend/app/ai/__init__.py
# PURPOSE:     Marks backend/app/ai as a package: the only place in the app that talks to an AI model.
# OWNER:       Mahadi (board row T3)
# DEPENDS ON:  Nothing.
# USED BY:     Routes import `extract_duties` from backend.app.ai.gateway (Maruf, T5).
# STATUS:      REAL
# DATA:        Synthetic only. No reason for leave, no medical or family details, ever.
# AI NOTE:     AGENTS.md rule 10: every model call goes through gateway.py. Never import a provider SDK
#              anywhere else in the app.
