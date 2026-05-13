from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from sqlalchemy.future import select
from sqlalchemy import update
from database import AsyncSessionLocal
from models import PendingPost
from services import extract_post_details, draft_linkedin_post
import re

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    welcome_text = (
        "Hello! I am your LinkedIn Post Manager.\n"
        "Just send me a message about what you did recently, and I'll add it to your pending list.\n\n"
        "Commands:\n"
        "/list - View your pending posts\n"
        "/draft <id> - Generate a draft for a specific post\n"
        "/done <id> - Mark a post as completed/posted"
    )
    await message.answer(welcome_text)

@router.message(Command("list"))
async def cmd_list(message: Message):
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(PendingPost).where(PendingPost.posted == False).order_by(PendingPost.id.asc())
        )
        posts = result.scalars().all()
        
    if not posts:
        await message.answer("You have no pending posts! Great job.")
        return
        
    response_lines = ["*Your Pending Posts:*"]
    for p in posts:
        date_str = p.created_at.strftime("%Y-%m-%d") if p.created_at else "Unknown Date"
        response_lines.append(f"*{p.id}.* [{date_str}] ***{p.title}*** --- {p.summary}")
        
    await message.answer("\n\n".join(response_lines), parse_mode="Markdown")

@router.message(Command("draft"))
async def cmd_draft(message: Message):
    args = message.text.split(maxsplit=1)
    if len(args) < 2 or not args[1].isdigit():
        await message.answer("Please provide a valid post ID. Example: `/draft 1`", parse_mode="Markdown")
        return
        
    post_id = int(args[1])
    
    async with AsyncSessionLocal() as session:
        post = await session.get(PendingPost, post_id)
        
    if not post or post.posted:
        await message.answer(f"Could not find an active pending post with ID {post_id}.")
        return

    await message.answer(f"Drafting LinkedIn post for: *{post.title}*...\nPlease wait, this may take a few seconds.", parse_mode="Markdown")
    
    result = await draft_linkedin_post(post.title, post.summary, post.raw_input)
    
    draft_text = result.get("draft", "Error generating draft.")
    media_recommendation = result.get("media_recommendation", "No media recommendation.")
    
    response_text = (
        f"**Draft for Post #{post.id}:**\n\n"
        f"{draft_text}\n\n"
        f"--- \n"
        f"**Media Recommendation:**\n"
        f"{media_recommendation}"
    )
    
    await message.answer(response_text)

@router.message(Command("done"))
async def cmd_done(message: Message):
    args = message.text.split(maxsplit=1)
    if len(args) < 2 or not args[1].isdigit():
        await message.answer("Please provide a valid post ID. Example: `/done 1`", parse_mode="Markdown")
        return
        
    post_id = int(args[1])
    
    async with AsyncSessionLocal() as session:
        post = await session.get(PendingPost, post_id)
        if not post or post.posted:
            await message.answer(f"Could not find an active pending post with ID {post_id}.")
            return
            
        post.posted = True
        await session.commit()
        
    await message.answer(f"Marked post #{post_id} as done! It has been removed from your pending list.")

@router.message(F.text)
async def handle_text(message: Message):
    # If the message starts with a command that wasn't caught, ignore
    if message.text.startswith('/'):
        return
        
    await message.answer("Extracting details and adding to your pending list...")
    
    details = await extract_post_details(message.text)
    
    async with AsyncSessionLocal() as session:
        new_post = PendingPost(
            raw_input=message.text,
            title=details.get("title", "Untitled"),
            summary=details.get("summary", "No summary provided")
        )
        session.add(new_post)
        await session.commit()
        await session.refresh(new_post)
        
    response = (
        f"✅ Added to your pending list!\n"
        f"*ID:* {new_post.id}\n"
        f"*Title:* {new_post.title}\n"
        f"*Summary:* {new_post.summary}"
    )
    
    await message.answer(response, parse_mode="Markdown")
