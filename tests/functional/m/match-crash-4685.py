import asyncio
import os


async def status(workers, session):
    await session.redis.publish(
        "_worker",
        f"{session.id} UP WORKER {os.getpid()} 0 {workers}"
    )

    pubsub = session.redis.pubsub()

    await pubsub.subscribe("_worker")
    async for msg in pubsub.listen():
        if msg is None or type(msg.get("data")) != bytes:
            continue
        msg = tuple(msg.get("data").decode("utf-8").split(" "))
        logger.debug(f"Got {msg}")
        match msg:
            # RabbitMQ going up has no session id yet
            case("NOSESSION", "UP", "RMQ", _):
                # Announce that we are up and sending to repeat a message
                logger.info("Sending RMQ info due to new worker")
                await session.redis.publish(
                    "_worker",
                    f"{session.id} UP WORKER {os.getpid()} 1 {workers}"
                )

            case(session_id, "REGET", "WORKER", reason):
                if session_id != session.id:  # noqa: F821
                    continue

                logger.warning(
                    f"RabbitMQ REGET: {reason}"  # noqa: F821
                )
                # Announce that we are up and sending to repeat a message
                await session.redis.publish(
                    "_worker",
                    f"{session.id} UP WORKER {os.getpid()} 1 {workers}"
                )

            # FUP = finally up
            case(session_id, "FUP", *worker_lst):
                logger.success("All workers are up!")
                if session_id != session.id:  # noqa: F821
                    continue

                # Finally up!
                try:
                    session.publish_workers(
                        [int(worker) for worker in worker_lst]  # noqa: F821
                    )

                except ValueError:
                    logger.warning(
                        f"Got invalid workers from rabbitmq ({workers})"
                    )

                await start_dbg(session)
                asyncio.create_task(vote_reminder(session))

            case _:
                pass  # Ignore the rest for now
