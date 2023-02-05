from typing import List, Dict, Type, Awaitable, Callable

from fastapi import Depends

from account.service_layer.uow import AbstractUnitOfWork, SqlAlchemyUnitOfWork
from account.service_layer.handlers import \
    EVENT_HANDLERS, COMMAND_HANDLERS
from account.domain import events, commands


class MessageBus:
    def __init__(
            self,
            uow: AbstractUnitOfWork = Depends(SqlAlchemyUnitOfWork),
            event_handlers: Dict[
                Type[events.Event],
                List[Callable[[events.Event, AbstractUnitOfWork], Awaitable]]
            ] = Depends(EVENT_HANDLERS),
            command_handlers: Dict[
                Type[commands.Command],
                Callable[[commands.Command, AbstractUnitOfWork], Awaitable]
            ] = Depends(COMMAND_HANDLERS),
    ):
        self.uow = uow
        self.event_handlers = event_handlers
        self.command_handlers = command_handlers

    async def handle(self, message: events.Event | commands.Command):
        self.queue = [message]
        while self.queue:
            message = self.queue.pop(0)
            if isinstance(message, events.Event):
                await self.handle_event(message)
            elif isinstance(message, commands.Command):
                await self.handle_command(message)
            else:
                raise Exception

    async def handle_event(self, event: events.Event):
        for handler in self.event_handlers[type(event)]:
            try:
                await handler(event, self.uow)
                self.queue.extend(self.uow.collect_new_events())
            except Exception:
                continue

    async def handle_command(self, command: commands.Command):
        try:
            handler = self.command_handlers[type(command)]
            await handler(command, self.uow)
            self.queue.extend(self.uow.collect_new_events())
        except Exception:
            raise
