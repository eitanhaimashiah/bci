import json


def parse_pose(context, snapshot):
    """Collects the translation and the rotation of the user's head
    at a given timestamp from `snapshot`, and publishes the result
    to a dedicated topic.

    Args:
        context (Context): Context in the application.
        snapshot (Snapshot): Snapshot uploaded to the server.

    """
    # TODO Check this function again
    context.save('pose.json', json.dumps(dict(
        translation=dict(
            x=snapshot.pose.translation.x,
            y=snapshot.pose.translation.y,
            z=snapshot.pose.translation.z,
        ),
        rotation=dict(
            x=snapshot.pose.rotation.x,
            y=snapshot.pose.rotation.y,
            z=snapshot.pose.rotation.z,
            w=snapshot.pose.rotation.w,
        )
    )))


parse_pose.field = 'pose'
