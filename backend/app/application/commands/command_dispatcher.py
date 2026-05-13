from app.application.commands.command import Command


class CommandDispatcher:

    async def dispatch(self, command: Command):
        return await command.execute()
