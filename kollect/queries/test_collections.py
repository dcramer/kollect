def test_no_params_results(gql_client, default_user):
    executed = gql_client.execute("""{ collections { id } }""", user=default_user)
    assert executed == {"data": {"collections": []}}


def test_id_with_result(gql_client, default_collection, default_user):
    executed = gql_client.execute(
        """{ collections(id:"%s") { id } }""" % (str(default_collection.id),),
        user=default_user,
    )
    assert executed == {"data": {"collections": [{"id": str(default_collection.id)}]}}


def test_id_and_num_items_with_result(
    gql_client, default_collection, default_item, default_user
):
    executed = gql_client.execute(
        """{ collections(id:"%s") { id, numItems } }""" % (str(default_collection.id),),
        user=default_user,
    )
    assert executed == {
        "data": {"collections": [{"id": str(default_collection.id), "numItems": 1}]}
    }


def test_id_with_no_result(gql_client, default_collection, default_user):
    executed = gql_client.execute(
        """{ collections(id:"74451c13-2a97-42a2-b136-03af6cbb4153") { id } }""",
        user=default_user,
    )
    assert executed == {"data": {"collections": []}}


def test_created_by_with_result(gql_client, default_collection, default_user):
    executed = gql_client.execute(
        """{ collections(createdBy:"%s") { id } }"""
        % (str(default_collection.created_by_id),),
        user=default_user,
    )
    assert executed == {"data": {"collections": [{"id": str(default_collection.id)}]}}


def test_created_by_with_no_result(gql_client, default_collection, default_user):
    executed = gql_client.execute(
        """{ collections(createdBy:"74451c13-2a97-42a2-b136-03af6cbb4153") { id } }""",
        user=default_user,
    )
    assert executed == {"data": {"collections": []}}
