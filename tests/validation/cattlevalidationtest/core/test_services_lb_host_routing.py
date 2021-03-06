from common_fixtures import *  # NOQA

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def test_lbservice_host_routing_1(admin_client, client, socat_containers):

    port = "900"

    service_scale = 2
    lb_scale = 1
    service_count = 4

    env, services, lb_service = create_env_with_multiple_svc_and_lb(
        client, service_scale, lb_scale, [port], service_count)

    service_link1 = {"serviceId": services[0].id,
                     "ports": ["www.abc1.com/service1.html",
                               "www.abc2.com/service2.html"]}
    service_link2 = {"serviceId": services[1].id,
                     "ports": ["www.abc1.com/service1.html",
                               "www.abc2.com/service2.html"]}
    service_link3 = {"serviceId": services[2].id,
                     "ports": ["www.abc3.com/service1.html",
                               "www.abc4.com/service2.html"]}
    service_link4 = {"serviceId": services[3].id,
                     "ports": ["www.abc3.com/service1.html",
                               "www.abc4.com/service2.html"]}

    lb_service.setservicelinks(
        serviceLinks=[service_link1, service_link2,
                      service_link3, service_link4])

    validate_add_service_link(admin_client, lb_service, services[0])
    validate_add_service_link(admin_client, lb_service, services[1])
    validate_add_service_link(admin_client, lb_service, services[2])
    validate_add_service_link(admin_client, lb_service, services[3])

    wait_for_lb_service_to_become_active(admin_client, client,
                                         services, lb_service)

    validate_lb_service(admin_client, client,
                        lb_service, port,
                        [services[0], services[1]],
                        "www.abc1.com", "/service1.html")

    validate_lb_service(admin_client, client,
                        lb_service, port, [services[0], services[1]],
                        "www.abc2.com", "/service2.html")

    validate_lb_service(admin_client, client,
                        lb_service, port, [services[2], services[3]],
                        "www.abc3.com", "/service1.html")

    validate_lb_service(admin_client, client,
                        lb_service, port, [services[2], services[3]],
                        "www.abc4.com", "/service2.html")
    delete_all(client, [env])


def test_lbservice_host_routing_cross_stack(
        admin_client, client, socat_containers):

    port = "901"

    service_scale = 2
    lb_scale = 1
    service_count = 4

    env, services, lb_service = create_env_with_multiple_svc_and_lb(
        client, service_scale, lb_scale, [port], service_count, True)

    service_link1 = {"serviceId": services[0].id,
                     "ports": ["www.abc1.com/service1.html",
                               "www.abc2.com/service2.html"]}
    service_link2 = {"serviceId": services[1].id,
                     "ports": ["www.abc1.com/service1.html",
                               "www.abc2.com/service2.html"]}
    service_link3 = {"serviceId": services[2].id,
                     "ports": ["www.abc3.com/service1.html",
                               "www.abc4.com/service2.html"]}
    service_link4 = {"serviceId": services[3].id,
                     "ports": ["www.abc3.com/service1.html",
                               "www.abc4.com/service2.html"]}

    lb_service.setservicelinks(
        serviceLinks=[service_link1, service_link2,
                      service_link3, service_link4])

    for service in services:
        service = service.activate()
    for service in services:
        service = client.wait_success(service, 120)
        assert service.state == "active"

    validate_add_service_link(admin_client, lb_service, services[0])
    validate_add_service_link(admin_client, lb_service, services[1])
    validate_add_service_link(admin_client, lb_service, services[2])
    validate_add_service_link(admin_client, lb_service, services[3])

    wait_for_lb_service_to_become_active(admin_client, client,
                                         services, lb_service)

    validate_lb_service(admin_client, client,
                        lb_service, port,
                        [services[0], services[1]],
                        "www.abc1.com", "/service1.html")

    validate_lb_service(admin_client, client,
                        lb_service, port, [services[0], services[1]],
                        "www.abc2.com", "/service2.html")

    validate_lb_service(admin_client, client,
                        lb_service, port, [services[2], services[3]],
                        "www.abc3.com", "/service1.html")

    validate_lb_service(admin_client, client,
                        lb_service, port, [services[2], services[3]],
                        "www.abc4.com", "/service2.html")
    to_delete = [env]
    for service in services:
        to_delete.append(get_env(admin_client, service))
    delete_all(client, to_delete)


def test_lbservice_host_routing_2(admin_client, client, socat_containers):

    port = "902"

    service_scale = 2
    lb_scale = 1
    service_count = 3

    env, services, lb_service = create_env_with_multiple_svc_and_lb(
        client, service_scale, lb_scale, [port], service_count)

    service_link1 = {"serviceId": services[0].id,
                     "ports": ["www.abc1.com/service1.html",
                               "www.abc2.com/service2.html"]}
    service_link2 = {"serviceId": services[1].id,
                     "ports": ["www.abc1.com/service1.html",
                               "www.abc2.com/service2.html"]}
    service_link3 = {"serviceId": services[2].id,
                     "ports": ["www.abc1.com/name.html",
                               "www.abc2.com/name.html"]}
    lb_service.setservicelinks(
        serviceLinks=[service_link1, service_link2,
                      service_link3])

    validate_add_service_link(admin_client, lb_service, services[0])
    validate_add_service_link(admin_client, lb_service, services[1])
    validate_add_service_link(admin_client, lb_service, services[2])

    wait_for_lb_service_to_become_active(admin_client, client,
                                         services, lb_service)

    validate_lb_service(admin_client, client,
                        lb_service, port, [services[0], services[1]],
                        "www.abc1.com", "/service1.html")

    validate_lb_service(admin_client, client,
                        lb_service, port, [services[0], services[1]],
                        "www.abc2.com", "/service2.html")

    validate_lb_service(admin_client, client,
                        lb_service, port, [services[2]],
                        "www.abc1.com", "/name.html")

    validate_lb_service(admin_client, client,
                        lb_service, port, [services[2]],
                        "www.abc2.com", "/name.html")

    validate_lb_service_for_no_access(admin_client, lb_service, port,
                                      "www.abc1.com",
                                      "/service2.html")
    validate_lb_service_for_no_access(admin_client, lb_service, port,
                                      "www.abc2.com",
                                      "/service1.html")
    delete_all(client, [env])


def test_lbservice_host_routing_scale_up(
        admin_client, client, socat_containers):

    port = "903"

    service_scale = 2
    lb_scale = 1
    service_count = 3

    env, services, lb_service = create_env_with_multiple_svc_and_lb(
        client, service_scale, lb_scale, [port], service_count)

    service_link1 = {"serviceId": services[0].id,
                     "ports": ["www.abc1.com/service1.html",
                               "www.abc2.com/service2.html"]}
    service_link2 = {"serviceId": services[1].id,
                     "ports": ["www.abc1.com/service1.html",
                               "www.abc2.com/service2.html"]}
    service_link3 = {"serviceId": services[2].id,
                     "ports": ["www.abc1.com/name.html",
                               "www.abc2.com/name.html"]}
    lb_service.setservicelinks(
        serviceLinks=[service_link1, service_link2,
                      service_link3])

    validate_add_service_link(admin_client, lb_service, services[0])
    validate_add_service_link(admin_client, lb_service, services[1])
    validate_add_service_link(admin_client, lb_service, services[2])

    wait_for_lb_service_to_become_active(admin_client, client,
                                         services, lb_service)

    validate_lb_service(admin_client, client,
                        lb_service, port, [services[0], services[1]],
                        "www.abc1.com", "/service1.html")

    validate_lb_service(admin_client, client,
                        lb_service, port, [services[0], services[1]],
                        "www.abc2.com", "/service2.html")

    validate_lb_service(admin_client, client,
                        lb_service, port, [services[2]],
                        "www.abc1.com", "/name.html")

    validate_lb_service(admin_client, client,
                        lb_service, port, [services[2]],
                        "www.abc2.com", "/name.html")

    validate_lb_service_for_no_access(admin_client, lb_service, port,
                                      "www.abc1.com",
                                      "/service2.html")
    validate_lb_service_for_no_access(admin_client, lb_service, port,
                                      "www.abc2.com",
                                      "/service1.html")
    final_service_scale = 3
    final_services = []
    for service in services:
        service = client.update(service, scale=final_service_scale,
                                name=service.name)
        service = client.wait_success(service, 120)
        assert service.state == "active"
        assert service.scale == final_service_scale
        final_services.append(service)

    wait_for_lb_service_to_become_active(admin_client, client,
                                         final_services,
                                         lb_service)

    validate_lb_service(admin_client, client, lb_service, port,
                        [final_services[0], final_services[1]],
                        "www.abc1.com", "/service1.html")

    validate_lb_service(admin_client, client,
                        lb_service, port,
                        [final_services[0], final_services[1]],
                        "www.abc2.com", "/service2.html")

    validate_lb_service(admin_client, client,
                        lb_service, port, [final_services[2]],
                        "www.abc1.com", "/name.html")

    validate_lb_service(admin_client, client,
                        lb_service, port, [final_services[2]],
                        "www.abc2.com", "/name.html")

    validate_lb_service_for_no_access(admin_client, lb_service, port,
                                      "www.abc1.com",
                                      "/service2.html")
    validate_lb_service_for_no_access(admin_client, lb_service, port,
                                      "www.abc2.com", "/service1.html")

    delete_all(client, [env])


def test_lbservice_host_routing_scale_down(
        admin_client, client, socat_containers):

    port = "904"

    service_scale = 3
    lb_scale = 1
    service_count = 3

    env, services, lb_service = create_env_with_multiple_svc_and_lb(
        client, service_scale, lb_scale, [port], service_count)

    service_link1 = {"serviceId": services[0].id,
                     "ports": ["www.abc1.com/service1.html",
                               "www.abc2.com/service2.html"]}
    service_link2 = {"serviceId": services[1].id,
                     "ports": ["www.abc1.com/service1.html",
                               "www.abc2.com/service2.html"]}
    service_link3 = {"serviceId": services[2].id,
                     "ports": ["www.abc1.com/name.html",
                               "www.abc2.com/name.html"]}
    lb_service.setservicelinks(
        serviceLinks=[service_link1, service_link2,
                      service_link3])

    validate_add_service_link(admin_client, lb_service, services[0])
    validate_add_service_link(admin_client, lb_service, services[1])
    validate_add_service_link(admin_client, lb_service, services[2])

    wait_for_lb_service_to_become_active(admin_client, client,
                                         services, lb_service)

    validate_lb_service(admin_client, client,
                        lb_service, port, [services[0], services[1]],
                        "www.abc1.com", "/service1.html")

    validate_lb_service(admin_client, client,
                        lb_service, port, [services[0], services[1]],
                        "www.abc2.com", "/service2.html")

    validate_lb_service(admin_client, client,
                        lb_service, port, [services[2]],
                        "www.abc1.com", "/name.html")

    validate_lb_service(admin_client, client,
                        lb_service, port, [services[2]],
                        "www.abc2.com", "/name.html")

    validate_lb_service_for_no_access(admin_client, lb_service, port,
                                      "www.abc1.com",
                                      "/service2.html")
    validate_lb_service_for_no_access(admin_client, lb_service, port,
                                      "www.abc2.com",
                                      "/service1.html")
    final_service_scale = 2
    final_services = []
    for service in services:
        service = client.update(service, scale=final_service_scale,
                                name=service.name)
        service = client.wait_success(service, 120)
        assert service.state == "active"
        assert service.scale == final_service_scale
        final_services.append(service)

    wait_for_lb_service_to_become_active(admin_client, client,
                                         final_services,
                                         lb_service)

    validate_lb_service(admin_client, client, lb_service, port,
                        [final_services[0], final_services[1]],
                        "www.abc1.com", "/service1.html")

    validate_lb_service(admin_client, client, lb_service, port,
                        [final_services[0], final_services[1]],
                        "www.abc2.com", "/service2.html")

    validate_lb_service(admin_client, client, lb_service,
                        port, [final_services[2]],
                        "www.abc1.com", "/name.html")

    validate_lb_service(admin_client, client, lb_service, port,
                        [final_services[2]],
                        "www.abc2.com", "/name.html")

    validate_lb_service_for_no_access(admin_client, lb_service, port,
                                      "www.abc1.com",
                                      "/service2.html")
    validate_lb_service_for_no_access(admin_client, lb_service, port,
                                      "www.abc2.com",
                                      "/service1.html")

    delete_all(client, [env])


def test_lbservice_host_routing_only_path(
        admin_client, client, socat_containers):

    port = "905"

    service_scale = 2
    lb_scale = 1
    service_count = 2

    env, services, lb_service = create_env_with_multiple_svc_and_lb(
        client, service_scale, lb_scale, [port], service_count)

    service_link1 = {"serviceId": services[0].id,
                     "ports": ["/service1.html"]}
    service_link2 = {"serviceId": services[1].id,
                     "ports": ["/service2.html"]}

    lb_service.setservicelinks(
        serviceLinks=[service_link1, service_link2])

    validate_add_service_link(admin_client, lb_service, services[0])
    validate_add_service_link(admin_client, lb_service, services[1])

    wait_for_lb_service_to_become_active(admin_client, client,
                                         services, lb_service)

    validate_lb_service(admin_client, client,
                        lb_service, port, [services[0]],
                        "www.abc1.com", "/service1.html")

    validate_lb_service(admin_client, client,
                        lb_service, port, [services[0]],
                        "www.abc2.com", "/service1.html")

    validate_lb_service(admin_client, client,
                        lb_service, port, [services[0]],
                        None, "/service1.html")

    validate_lb_service(admin_client, client,
                        lb_service, port, [services[1]],
                        "www.abc3.com", "/service2.html")

    validate_lb_service(admin_client, client,
                        lb_service, port,  [services[1]],
                        "www.abc2.com", "/service2.html")

    validate_lb_service(admin_client, client,
                        lb_service, port, [services[0]],
                        None, "/service1.html")

    validate_lb_service_for_no_access(admin_client, lb_service, port,
                                      "www.abc3.com", "/name.html")

    delete_all(client, [env])


def test_lbservice_host_routing_only_host(
        admin_client, client, socat_containers):

    port = "906"

    service_scale = 2
    lb_scale = 1
    service_count = 2

    env, services, lb_service = create_env_with_multiple_svc_and_lb(
        client, service_scale, lb_scale, [port], service_count)

    service_link1 = {"serviceId": services[0].id,
                     "ports": ["www.abc.com"]}
    service_link2 = {"serviceId": services[1].id,
                     "ports": ["www.abc1.com"]}

    lb_service.setservicelinks(
        serviceLinks=[service_link1, service_link2])

    validate_add_service_link(admin_client, lb_service, services[0])
    validate_add_service_link(admin_client, lb_service, services[1])

    wait_for_lb_service_to_become_active(admin_client, client,
                                         [services[0], services[1]],
                                         lb_service)

    validate_lb_service(admin_client, client,
                        lb_service, port, [services[0]],
                        "www.abc.com", "/service1.html")

    validate_lb_service(admin_client, client,
                        lb_service, port, [services[0]],
                        "www.abc.com", "/service2.html")

    validate_lb_service(admin_client, client,
                        lb_service, port, [services[1]],
                        "www.abc1.com", "/name.html")

    validate_lb_service_for_no_access(admin_client, lb_service, port,
                                      "www.abc2.com", "/name.html")

    delete_all(client, [env])


def test_lbservice_host_routing_3(admin_client, client, socat_containers):

    port = "907"

    service_scale = 2
    lb_scale = 1
    service_count = 4

    env, services, lb_service = create_env_with_multiple_svc_and_lb(
        client, service_scale, lb_scale, [port], service_count)

    service_link1 = {"serviceId": services[0].id,
                     "ports": ["www.abc.com"]}
    service_link2 = {"serviceId": services[1].id,
                     "ports": ["www.abc1.com"]}
    service_link3 = {"serviceId": services[2].id}
    service_link4 = {"serviceId": services[3].id,
                     "ports": ["/service1.html"]}

    lb_service.setservicelinks(
        serviceLinks=[service_link1, service_link2,
                      service_link3, service_link4])

    validate_add_service_link(admin_client, lb_service, services[0])
    validate_add_service_link(admin_client, lb_service, services[1])
    validate_add_service_link(admin_client, lb_service, services[2])
    validate_add_service_link(admin_client, lb_service, services[3])
    wait_for_lb_service_to_become_active(admin_client, client,
                                         services, lb_service)
    validate_lb_service(admin_client, client,
                        lb_service, port, [services[0]],
                        "www.abc.com", "/service2.html")

    validate_lb_service(admin_client, client,
                        lb_service, port, [services[1]],
                        "www.abc1.com", "/name.html")

    validate_lb_service(admin_client, client,
                        lb_service, port, [services[2]],
                        "www.abc2.com", "/name.html")

    validate_lb_service(admin_client, client,
                        lb_service, port, [services[3]],
                        "www.abc3.com", "/service1.html")

    delete_all(client, [env])


def test_lbservice_edit_host_routing_3(admin_client, client, socat_containers):

    port = "908"

    service_scale = 2
    lb_scale = 1
    service_count = 5

    env, services, lb_service = create_env_with_multiple_svc_and_lb(
        client, service_scale, lb_scale, [port], service_count)

    service_link1 = {"serviceId": services[0].id,
                     "ports": ["www.abc.com"]}
    service_link2 = {"serviceId": services[1].id,
                     "ports": ["www.abc1.com"]}
    service_link3 = {"serviceId": services[2].id}
    service_link4 = {"serviceId": services[3].id,
                     "ports": ["/service1.html"]}

    lb_service.setservicelinks(
        serviceLinks=[service_link1, service_link2,
                      service_link3, service_link4])

    validate_add_service_link(admin_client, lb_service, services[0])
    validate_add_service_link(admin_client, lb_service, services[1])
    validate_add_service_link(admin_client, lb_service, services[2])
    validate_add_service_link(admin_client, lb_service, services[3])

    service_list = [services[0], services[1], services[2], services[3]]
    wait_for_lb_service_to_become_active(admin_client, client,
                                         service_list,
                                         lb_service)
    validate_lb_service(admin_client, client, lb_service,
                        port, [services[0]],
                        "www.abc.com", "/service2.html")

    validate_lb_service(admin_client, client,
                        lb_service, port, [services[1]],
                        "www.abc1.com", "/name.html")

    validate_lb_service(admin_client, client,
                        lb_service, port, [services[2]],
                        "www.abc2.com", "/name.html")

    validate_lb_service(admin_client, client,
                        lb_service, port, [services[3]],
                        "www.abc3.com", "/service1.html")

    # Edit service links
    service_link1 = {"serviceId": services[0].id,
                     "ports": ["www.abc.com"]}
    service_link2 = {"serviceId": services[2].id}
    service_link3 = {"serviceId": services[3].id,
                     "ports": ["/service2.html"]}
    service_link4 = {"serviceId": services[4].id,
                     "ports": ["www.abc.com", "www.abc1.com"]}

    lb_service.setservicelinks(
        serviceLinks=[service_link1, service_link2,
                      service_link3, service_link4])

    validate_add_service_link(admin_client, lb_service, services[0])
    validate_add_service_link(admin_client, lb_service, services[4])
    validate_add_service_link(admin_client, lb_service, services[2])
    validate_add_service_link(admin_client, lb_service, services[3])

    service_list = [services[0], services[2], services[3], services[4]]

    wait_for_lb_service_to_become_active(admin_client, client,
                                         service_list,
                                         lb_service)
    validate_lb_service(admin_client, client,
                        lb_service, port, [services[0], services[4]],
                        "www.abc.com", "/service1.html")

    validate_lb_service(admin_client, client,
                        lb_service, port, [services[4]],
                        "www.abc1.com", "/name.html")

    validate_lb_service(admin_client, client,
                        lb_service, port, [services[2]],
                        "www.abc2.com", "/name.html")

    validate_lb_service(admin_client, client,
                        lb_service, port, [services[3]],
                        "www.abc3.com", "/service2.html")

    delete_all(client, [env])


def test_lbservice_edit_host_routing_add_host(
        admin_client, client, socat_containers):

    port = "909"

    service_scale = 2
    lb_scale = 1
    service_count = 1

    env, services, lb_service = create_env_with_multiple_svc_and_lb(
        client, service_scale, lb_scale, [port], service_count)

    service_link1 = {"serviceId": services[0].id,
                     "ports": ["www.abc.com"]}

    lb_service.setservicelinks(
        serviceLinks=[service_link1])

    validate_add_service_link(admin_client, lb_service, services[0])

    wait_for_lb_service_to_become_active(admin_client, client,
                                         services, lb_service)
    validate_lb_service(admin_client, client,
                        lb_service, port, [services[0]],
                        "www.abc.com", "/service2.html")
    validate_lb_service_for_no_access(admin_client, lb_service, port,
                                      "www.abc2.com", "/name.html")
    validate_lb_service_for_no_access(admin_client, lb_service, port,
                                      "www.abc3.com", "/name.html")

    # Edit service links
    service_link1 = {"serviceId": services[0].id,
                     "ports": ["www.abc.com", "www.abc2.com"]}

    lb_service.setservicelinks(
        serviceLinks=[service_link1])

    validate_add_service_link(admin_client, lb_service, services[0])
    wait_for_lb_service_to_become_active(admin_client, client,
                                         services, lb_service)
    validate_lb_service(admin_client, client,
                        lb_service, port, [services[0]],
                        "www.abc.com", "/service2.html")
    validate_lb_service(admin_client, client,
                        lb_service, port, [services[0]],
                        "www.abc2.com", "/name.html")

    validate_lb_service_for_no_access(admin_client, lb_service, port,
                                      "www.abc3.com", "/name.html")

    delete_all(client, [env])


def test_lbservice_edit_host_routing_remove_host(
        admin_client, client, socat_containers):

    port = "910"

    service_scale = 2
    lb_scale = 1
    service_count = 1

    env, services, lb_service = create_env_with_multiple_svc_and_lb(
        client, service_scale, lb_scale, [port], service_count)

    service_link1 = {"serviceId": services[0].id,
                     "ports": ["www.abc.com", "www.abc2.com"]}

    lb_service.setservicelinks(
        serviceLinks=[service_link1])

    validate_add_service_link(admin_client, lb_service, services[0])
    wait_for_lb_service_to_become_active(admin_client, client, services,
                                         lb_service)
    validate_lb_service(admin_client, client,
                        lb_service, port, [services[0]],
                        "www.abc.com", "/service2.html")
    validate_lb_service(admin_client, client,
                        lb_service, port, [services[0]],
                        "www.abc2.com", "/service2.html")
    validate_lb_service_for_no_access(admin_client, lb_service, port,
                                      "www.abc3.com", "/name.html")

    # Edit service links
    service_link1 = {"serviceId": services[0].id,
                     "ports": ["www.abc.com"]}

    lb_service.setservicelinks(
        serviceLinks=[service_link1])

    wait_for_lb_service_to_become_active(admin_client, client,
                                         services, lb_service)
    validate_add_service_link(admin_client, lb_service, services[0])

    validate_lb_service(admin_client, client,
                        lb_service, port, [services[0]],
                        "www.abc.com", "/service2.html")
    validate_lb_service_for_no_access(admin_client, lb_service, port,
                                      "www.abc2.com", "/name.html")

    delete_all(client, [env])


def test_lbservice_edit_host_routing_edit_existing_host(
        admin_client, client, socat_containers):

    port = "911"

    service_scale = 2
    lb_scale = 1
    service_count = 1

    env, services, lb_service = create_env_with_multiple_svc_and_lb(
        client, service_scale, lb_scale, [port], service_count)

    service_link1 = {"serviceId": services[0].id,
                     "ports": ["www.abc.com"]}

    lb_service.setservicelinks(
        serviceLinks=[service_link1])

    wait_for_lb_service_to_become_active(admin_client, client,
                                         services, lb_service)
    validate_add_service_link(admin_client, lb_service, services[0])

    validate_lb_service(admin_client, client,
                        lb_service, port, [services[0]],
                        "www.abc.com", "/service2.html")
    validate_lb_service_for_no_access(admin_client, lb_service, port,
                                      "www.abc2.com", "/name.html")

    # Edit service links
    service_link1 = {"serviceId": services[0].id,
                     "ports": ["www.abc2.com"]}

    lb_service.setservicelinks(
        serviceLinks=[service_link1])

    validate_add_service_link(admin_client, lb_service, services[0])
    wait_for_lb_service_to_become_active(admin_client, client,
                                         services, lb_service)
    validate_lb_service(admin_client, client,
                        lb_service, port, [services[0]],
                        "www.abc2.com", "/service2.html")
    validate_lb_service_for_no_access(admin_client, lb_service, port,
                                      "www.abc.com", "/name.html")

    delete_all(client, [env])


def test_lbservice_host_routing_multiple_port_1(
        admin_client, client, socat_containers):

    port1 = "1000"
    port2 = "1001"

    port1_target = "80"
    port2_target = "81"

    service_scale = 2
    lb_scale = 1
    service_count = 4

    env, services, lb_service = \
        create_env_with_multiple_svc_and_lb(
            client, service_scale, lb_scale, [port1, port2], service_count)

    service_link1 = {"serviceId": services[0].id,
                     "ports": ["www.abc1.com:"+port1+"/service1.html",
                               "www.abc1.com:"+port2+"/service3.html"]}
    service_link2 = {"serviceId": services[1].id,
                     "ports": ["www.abc2.com"]}
    service_link3 = {"serviceId": services[2].id,
                     "ports": ["/service1.html="+port1_target,
                               "/service3.html="+port2_target]}
    service_link4 = {"serviceId": services[3].id}

    lb_service.setservicelinks(
        serviceLinks=[service_link1, service_link2,
                      service_link3, service_link4])

    validate_add_service_link(admin_client, lb_service, services[0])
    validate_add_service_link(admin_client, lb_service, services[1])
    validate_add_service_link(admin_client, lb_service, services[2])
    validate_add_service_link(admin_client, lb_service, services[3])

    wait_for_lb_service_to_become_active(admin_client, client,
                                         services, lb_service)
    validate_lb_service(admin_client, client,
                        lb_service, port1,
                        [services[0]],
                        "www.abc1.com", "/service1.html")
    validate_lb_service(admin_client, client,
                        lb_service, port1, [services[3]],
                        "www.abc1.com", "/service2.html")
    validate_lb_service(admin_client, client,
                        lb_service, port1, [services[1]],
                        "www.abc2.com", "/service1.html")
    validate_lb_service(admin_client, client,
                        lb_service, port1, [services[1]],
                        "www.abc2.com", "/service2.html")
    validate_lb_service(admin_client, client,
                        lb_service, port2, [services[1]],
                        "www.abc2.com", "/service3.html")
    validate_lb_service(admin_client, client,
                        lb_service, port2,
                        [services[0]],
                        "www.abc1.com", "/service3.html")
    validate_lb_service(admin_client, client,
                        lb_service, port2, [services[2]],
                        "www.abc4.com", "/service3.html")
    validate_lb_service(admin_client, client,
                        lb_service, port2, [services[3]],
                        "www.abc3.com", "/service4.html")

    delete_all(client, [env])


def test_lbservice_host_routing_multiple_port_2(
        admin_client, client, socat_containers):

    port1 = "1002"
    port2 = "1003"

    service_scale = 2
    lb_scale = 1
    service_count = 3

    env, services, lb_service = \
        create_env_with_multiple_svc_and_lb(
            client, service_scale, lb_scale, [port1, port2], service_count)

    service_link1 = {"serviceId": services[0].id,
                     "ports": ["/81"]}
    service_link2 = {"serviceId": services[1].id,
                     "ports": ["/81/service3.html"]}
    service_link3 = {"serviceId": services[2].id,
                     "ports": ["/service"]}

    lb_service.setservicelinks(
        serviceLinks=[service_link1, service_link2, service_link3])

    wait_for_lb_service_to_become_active(admin_client, client,
                                         services, lb_service)
    validate_add_service_link(admin_client, lb_service, services[0])
    validate_add_service_link(admin_client, lb_service, services[1])
    validate_add_service_link(admin_client, lb_service, services[2])

    validate_lb_service(admin_client, client,
                        lb_service, port1,
                        [services[2]],
                        "www.abc1.com", "/service1.html")
    validate_lb_service(admin_client, client,
                        lb_service, port1, [services[0]],
                        "www.abc1.com", "/81/service4.html")
    validate_lb_service(admin_client, client,
                        lb_service, port1, [services[1]],
                        "www.abc1.com", "/81/service3.html")

    validate_lb_service(admin_client, client,
                        lb_service, port2, [services[2]],
                        "www.abc1.com", "/service3.html")

    validate_lb_service(admin_client, client,
                        lb_service, port2, [services[2]],
                        "www.abc1.com", "/service4.html")

    delete_all(client, [env])


def test_lbservice_host_routing_multiple_port_3(
        admin_client, client, socat_containers):

    port1 = "1004"
    port2 = "1005"

    service_scale = 2
    lb_scale = 1
    service_count = 2

    env, services, lb_service = \
        create_env_with_multiple_svc_and_lb(
            client, service_scale, lb_scale, [port1, port2], service_count)

    service_link1 = {"serviceId": services[0].id}
    service_link2 = {"serviceId": services[1].id}

    lb_service.setservicelinks(
        serviceLinks=[service_link1, service_link2])

    wait_for_lb_service_to_become_active(admin_client, client,
                                         services, lb_service)
    validate_add_service_link(admin_client, lb_service, services[0])
    validate_add_service_link(admin_client, lb_service, services[1])

    validate_lb_service(admin_client, client,
                        lb_service, port1,
                        [services[0], services[1]],
                        "www.abc1.com", "/service1.html")
    validate_lb_service(admin_client, client,
                        lb_service, port2,
                        [services[0], services[1]],
                        "www.abc1.com", "/service3.html")
    delete_all(client, [env])


def test_lbservice_host_routing_target_port_override(
        admin_client, client, socat_containers):

    port1 = "1010"

    service_scale = 2
    lb_scale = 1
    service_count = 2

    env, services, lb_service = \
        create_env_with_multiple_svc_and_lb(
            client, service_scale, lb_scale, [port1], service_count)

    service_link1 = {"serviceId": services[0].id,
                     "ports": ["/service3.html=81"]}
    service_link2 = {"serviceId": services[1].id}

    lb_service.setservicelinks(
        serviceLinks=[service_link1, service_link2])

    wait_for_lb_service_to_become_active(admin_client, client,
                                         services, lb_service)
    validate_add_service_link(admin_client, lb_service, services[0])
    validate_add_service_link(admin_client, lb_service, services[1])

    validate_lb_service(admin_client, client,
                        lb_service, port1,
                        [services[1]],
                        "www.abc1.com", "/service1.html")
    validate_lb_service(admin_client, client,
                        lb_service, port1,
                        [services[0]],
                        "www.abc1.com", "/service3.html")
    delete_all(client, [env])


def test_lbservice_host_routing_multiple_port_1_edit_add(
        admin_client, client, socat_containers):

    port1 = "1006"
    port2 = "1007"

    port1_target = "80"
    port2_target = "81"

    service_scale = 2
    lb_scale = 1
    service_count = 5

    env, services, lb_service = \
        create_env_with_multiple_svc_and_lb(
            client, service_scale, lb_scale, [port1, port2], service_count)

    service_link1 = {"serviceId": services[0].id,
                     "ports": ["www.abc1.com:"+port1+"/service1.html",
                               "www.abc1.com:"+port2+"/service3.html"]}
    service_link2 = {"serviceId": services[1].id,
                     "ports": ["www.abc1.com"]}
    service_link3 = {"serviceId": services[2].id,
                     "ports": ["/service1.html="+port1_target,
                               "/service3.html="+port2_target]}
    service_link4 = {"serviceId": services[3].id}

    lb_service.setservicelinks(
        serviceLinks=[service_link1, service_link2,
                      service_link3, service_link4])

    validate_add_service_link(admin_client, lb_service, services[0])
    validate_add_service_link(admin_client, lb_service, services[1])
    validate_add_service_link(admin_client, lb_service, services[2])
    validate_add_service_link(admin_client, lb_service, services[3])

    service_list = [services[0], services[1], services[2], services[3]]
    wait_for_lb_service_to_become_active(admin_client, client,
                                         service_list, lb_service)
    validate_lb_service(admin_client, client,
                        lb_service, port1,
                        [services[0]],
                        "www.abc1.com", "/service1.html")
    validate_lb_service(admin_client, client,
                        lb_service, port1, [services[1]],
                        "www.abc1.com", "/service2.html")
    validate_lb_service(admin_client, client,
                        lb_service, port1, [services[2]],
                        "www.abc2.com", "/service1.html")
    validate_lb_service(admin_client, client,
                        lb_service, port1, [services[3]],
                        "www.abc2.com", "/service2.html")

    validate_lb_service(admin_client, client,
                        lb_service, port2,
                        [services[0]],
                        "www.abc1.com", "/service3.html")
    validate_lb_service(admin_client, client,
                        lb_service, port2, [services[1]],
                        "www.abc1.com", "/service4.html")
    validate_lb_service(admin_client, client,
                        lb_service, port2, [services[2]],
                        "www.abc2.com", "/service3.html")
    validate_lb_service(admin_client, client,
                        lb_service, port2, [services[3]],
                        "www.abc2.com", "/service4.html")

    service_link1 = {"serviceId": services[0].id,
                     "ports": ["www.abc1.com:"+port1+"/service1.html",
                               "www.abc1.com:"+port2+"/service3.html",
                               "www.abc2.com:"+port1+"/service1.html",
                               "www.abc2.com:"+port2+"/service3.html"]}
    service_link2 = {"serviceId": services[1].id,
                     "ports": ["www.abc1.com", "www.abc2.com"]}
    service_link3 = {"serviceId": services[2].id,
                     "ports": ["/service1.html="+port1_target,
                               "/service3.html="+port2_target]}
    service_link4 = {"serviceId": services[3].id}
    service_link5 = {"serviceId": services[4].id}

    lb_service.setservicelinks(
        serviceLinks=[service_link1, service_link2,
                      service_link3, service_link4, service_link5])

    validate_add_service_link(admin_client, lb_service, services[0])
    validate_add_service_link(admin_client, lb_service, services[1])
    validate_add_service_link(admin_client, lb_service, services[2])
    validate_add_service_link(admin_client, lb_service, services[3])
    validate_add_service_link(admin_client, lb_service, services[4])
    wait_for_lb_service_to_become_active(admin_client, client,
                                         services, lb_service)
    validate_lb_service(admin_client, client,
                        lb_service, port1,
                        [services[0]],
                        "www.abc1.com", "/service1.html")
    validate_lb_service(admin_client, client,
                        lb_service, port1, [services[1]],
                        "www.abc1.com", "/service2.html")
    validate_lb_service(admin_client, client,
                        lb_service, port1, [services[0]],
                        "www.abc2.com", "/service1.html")
    validate_lb_service(admin_client, client,
                        lb_service, port1, [services[1]],
                        "www.abc2.com", "/service2.html")
    validate_lb_service(admin_client, client,
                        lb_service, port1, [services[3], services[4]],
                        "www.abc3.com", "/service2.html")

    validate_lb_service(admin_client, client,
                        lb_service, port2,
                        [services[0]],
                        "www.abc1.com", "/service3.html")
    validate_lb_service(admin_client, client,
                        lb_service, port2, [services[1]],
                        "www.abc1.com", "/service4.html")
    validate_lb_service(admin_client, client,
                        lb_service, port2, [services[0]],
                        "www.abc2.com", "/service3.html")
    validate_lb_service(admin_client, client,
                        lb_service, port2, [services[1]],
                        "www.abc2.com", "/service4.html")
    validate_lb_service(admin_client, client,
                        lb_service, port2, [services[3], services[4]],
                        "www.abc3.com", "/service4.html")

    delete_all(client, [env])


def test_lbservice_host_routing_multiple_port_1_edit_edit(
        admin_client, client, socat_containers):

    port1 = "1008"
    port2 = "1009"

    port1_target = "80"
    port2_target = "81"

    service_scale = 2
    lb_scale = 1
    service_count = 5

    env, services, lb_service = \
        create_env_with_multiple_svc_and_lb(
            client, service_scale, lb_scale, [port1, port2], service_count)

    service_link1 = {"serviceId": services[0].id,
                     "ports": ["www.abc1.com:"+port1+"/service1.html",
                               "www.abc1.com:"+port2+"/service3.html"]}
    service_link2 = {"serviceId": services[1].id,
                     "ports": ["www.abc1.com"]}
    service_link3 = {"serviceId": services[2].id,
                     "ports": ["/service1.html="+port1_target,
                               "/service3.html="+port2_target]}
    service_link4 = {"serviceId": services[3].id}

    lb_service.setservicelinks(
        serviceLinks=[service_link1, service_link2,
                      service_link3, service_link4])

    validate_add_service_link(admin_client, lb_service, services[0])
    validate_add_service_link(admin_client, lb_service, services[1])
    validate_add_service_link(admin_client, lb_service, services[2])
    validate_add_service_link(admin_client, lb_service, services[3])

    service_list = [services[0], services[1], services[2], services[3]]
    wait_for_lb_service_to_become_active(admin_client, client,
                                         service_list, lb_service)
    validate_lb_service(admin_client, client,
                        lb_service, port1,
                        [services[0]],
                        "www.abc1.com", "/service1.html")
    validate_lb_service(admin_client, client,
                        lb_service, port1, [services[1]],
                        "www.abc1.com", "/service2.html")
    validate_lb_service(admin_client, client,
                        lb_service, port1, [services[2]],
                        "www.abc2.com", "/service1.html")
    validate_lb_service(admin_client, client,
                        lb_service, port1, [services[3]],
                        "www.abc2.com", "/service2.html")

    validate_lb_service(admin_client, client,
                        lb_service, port2,
                        [services[0]],
                        "www.abc1.com", "/service3.html")
    validate_lb_service(admin_client, client,
                        lb_service, port2, [services[1]],
                        "www.abc1.com", "/service4.html")
    validate_lb_service(admin_client, client,
                        lb_service, port2, [services[2]],
                        "www.abc2.com", "/service3.html")
    validate_lb_service(admin_client, client,
                        lb_service, port2, [services[3]],
                        "www.abc2.com", "/service4.html")

    service_link1 = {"serviceId": services[0].id,
                     "ports": ["www.abc2.com:"+port1+"/service1.html",
                               "www.abc2.com:"+port2+"/service3.html"]}
    service_link2 = {"serviceId": services[1].id,
                     "ports": ["www.abc3.com"]}
    service_link3 = {"serviceId": services[2].id,
                     "ports": ["/service2.html="+port1_target,
                               "/service4.html="+port2_target]}
    service_link4 = {"serviceId": services[3].id}
    service_link5 = {"serviceId": services[4].id}

    lb_service.setservicelinks(
        serviceLinks=[service_link1, service_link2,
                      service_link3, service_link4, service_link5])

    validate_add_service_link(admin_client, lb_service, services[0])
    validate_add_service_link(admin_client, lb_service, services[1])
    validate_add_service_link(admin_client, lb_service, services[2])
    validate_add_service_link(admin_client, lb_service, services[3])
    validate_add_service_link(admin_client, lb_service, services[4])
    wait_for_lb_service_to_become_active(admin_client, client,
                                         services, lb_service)
    validate_lb_service(admin_client, client,
                        lb_service, port1,
                        [services[0]],
                        "www.abc2.com", "/service1.html")
    validate_lb_service(admin_client, client,
                        lb_service, port1, [services[2]],
                        "www.abc2.com", "/service2.html")
    validate_lb_service(admin_client, client,
                        lb_service, port1, [services[3], services[4]],
                        "www.abc1.com", "/service1.html")
    validate_lb_service(admin_client, client,
                        lb_service, port1, [services[2]],
                        "www.abc1.com", "/service2.html")
    validate_lb_service(admin_client, client,
                        lb_service, port1, [services[1]],
                        "www.abc3.com", "/service1.html")

    validate_lb_service(admin_client, client,
                        lb_service, port2,
                        [services[0]],
                        "www.abc2.com", "/service3.html")
    validate_lb_service(admin_client, client,
                        lb_service, port2, [services[2]],
                        "www.abc2.com", "/service4.html")
    validate_lb_service(admin_client, client,
                        lb_service, port2, [services[3], services[4]],
                        "www.abc1.com", "/service3.html")
    validate_lb_service(admin_client, client,
                        lb_service, port2, [services[2]],
                        "www.abc1.com", "/service4.html")
    validate_lb_service(admin_client, client,
                        lb_service, port2, [services[1]],
                        "www.abc3.com", "/service3.html")

    delete_all(client, [env])


def test_lbservice_external_service(admin_client, client, socat_containers):
    port = "1010"

    lb_scale = 2

    env, lb_service, ext_service, con_list = \
        create_env_with_ext_svc_and_lb(client, lb_scale, port)

    ext_service = activate_svc(client, ext_service)
    lb_service = activate_svc(client, lb_service)

    lb_service.setservicelinks(serviceLinks=[{"serviceId": ext_service.id}])

    validate_add_service_link(admin_client, lb_service, ext_service)

    """
    # Wait for host maps to be created
    lbs = client.list_loadBalancer(serviceId=lb_service.id)
    assert len(lbs) == 1
    lb = lbs[0]
    host_maps = wait_until_host_map_created(client, lb, lb_service.scale, 60)
    assert len(host_maps) == lb_service.scale
    """

    validate_lb_service_for_external_services(admin_client, client,
                                              lb_service, port, con_list)

    delete_all(client, [env])


def test_lbservice_host_routing_tcp_only(admin_client, client,
                                         socat_containers):

    port = "1011/tcp"

    service_scale = 2
    lb_scale = 1
    service_count = 2

    env, services, lb_service = create_env_with_multiple_svc_and_lb(
        client, service_scale, lb_scale, [port], service_count)

    service_link1 = {"serviceId": services[0].id,
                     "ports": ["www.abc1.com/service1.html",
                               "www.abc2.com/service2.html"]}
    service_link2 = {"serviceId": services[1].id,
                     "ports": ["www.abc1.com/service1.html",
                               "www.abc2.com/service2.html"]}

    lb_service.setservicelinks(
        serviceLinks=[service_link1, service_link2])

    validate_add_service_link(admin_client, lb_service, services[0])
    validate_add_service_link(admin_client, lb_service, services[1])

    wait_for_lb_service_to_become_active(admin_client, client,
                                         services, lb_service)

    port = "1011"
    validate_lb_service(admin_client, client,
                        lb_service, port,
                        [services[0], services[1]])

    validate_lb_service(admin_client, client,
                        lb_service, port, [services[0], services[1]])

    delete_all(client, [env])


def test_lbservice_host_routing_tcp_and_http(admin_client, client,
                                             socat_containers):

    port1 = "1012/tcp"
    port2 = "1013"

    service_scale = 2
    lb_scale = 1
    service_count = 2

    env, services, lb_service = create_env_with_multiple_svc_and_lb(
        client, service_scale, lb_scale, [port1, port2], service_count)

    service_link1 = {"serviceId": services[0].id,
                     "ports": ["www.abc1.com/service3.html"]}
    service_link2 = {"serviceId": services[1].id,
                     "ports": ["www.abc1.com/service4.html"]}

    lb_service.setservicelinks(
        serviceLinks=[service_link1, service_link2])

    validate_add_service_link(admin_client, lb_service, services[0])
    validate_add_service_link(admin_client, lb_service, services[1])

    wait_for_lb_service_to_become_active(admin_client, client,
                                         services, lb_service)

    port1 = "1012"
    validate_lb_service(admin_client, client,
                        lb_service, port1,
                        [services[0], services[1]])

    validate_lb_service(admin_client, client,
                        lb_service, port1,
                        [services[0], services[1]])

    validate_lb_service(admin_client, client,
                        lb_service, port2,
                        [services[0]],
                        "www.abc1.com", "/service3.html")

    validate_lb_service(admin_client, client,
                        lb_service, port2, [services[1]],
                        "www.abc1.com", "/service4.html")

    validate_lb_service_for_no_access(admin_client, lb_service, port2,
                                      "www.abc2.com",
                                      "/service3.html")
    delete_all(client, [env])


def test_lbservice_host_routing_wildcard(
        admin_client, client, socat_containers):

    port = "1014"

    service_scale = 2
    lb_scale = 1
    service_count = 3

    env, services, lb_service = create_env_with_multiple_svc_and_lb(
        client, service_scale, lb_scale, [port], service_count)

    service_link1 = {"serviceId": services[0].id,
                     "ports": ["*.domain.com"]}
    service_link2 = {"serviceId": services[1].id,
                     "ports": ["domain.*"]}
    service_link3 = {"serviceId": services[2].id,
                     "ports": ["abc.domain.com"]}

    lb_service.setservicelinks(
        serviceLinks=[service_link1, service_link2, service_link3])

    validate_add_service_link(admin_client, lb_service, services[0])
    validate_add_service_link(admin_client, lb_service, services[1])
    validate_add_service_link(admin_client, lb_service, services[2])

    wait_for_lb_service_to_become_active(admin_client, client,
                                         services, lb_service)

    validate_lb_service(admin_client, client,
                        lb_service, port,
                        [services[2]],
                        "abc.domain.com", "/name.html")

    validate_lb_service(admin_client, client,
                        lb_service, port,
                        [services[0]],
                        "abc.def.domain.com", "/service1.html")

    validate_lb_service(admin_client, client,
                        lb_service, port,
                        [services[1]],
                        "domain.abc.def.com", "/service1.html")

    validate_lb_service(admin_client, client,
                        lb_service, port,
                        [services[1]],
                        "domain.abc.com", "/name.html")
    delete_all(client, [env])


def test_lbservice_host_routing_wildcard_order(
        admin_client, client, socat_containers):

    port = "1014"

    service_scale = 2
    lb_scale = 1
    service_count = 5

    env, services, lb_service = create_env_with_multiple_svc_and_lb(
        client, service_scale, lb_scale, [port], service_count)

    service_link1 = {"serviceId": services[0].id,
                     "ports": ["*.domain.com"]}
    service_link2 = {"serviceId": services[1].id,
                     "ports": ["domain.*"]}
    service_link3 = {"serviceId": services[2].id,
                     "ports": ["abc.domain.com"]}
    service_link4 = {"serviceId": services[3].id,
                     "ports": ["abc.domain.com/service1.html"]}
    service_link5 = {"serviceId": services[4].id,
                     "ports": ["*.domain.com/service1.html"]}

    lb_service.setservicelinks(
        serviceLinks=[service_link1, service_link2,
                      service_link3, service_link4, service_link5])

    validate_add_service_link(admin_client, lb_service, services[0])
    validate_add_service_link(admin_client, lb_service, services[1])
    validate_add_service_link(admin_client, lb_service, services[2])
    validate_add_service_link(admin_client, lb_service, services[3])
    validate_add_service_link(admin_client, lb_service, services[4])

    wait_for_lb_service_to_become_active(admin_client, client,
                                         services, lb_service)

    validate_lb_service(admin_client, client,
                        lb_service, port,
                        [services[4]],
                        "abc.def.domain.com", "/service1.html")

    validate_lb_service(admin_client, client,
                        lb_service, port,
                        [services[0]],
                        "abc.def.domain.com", "/name.html")

    validate_lb_service(admin_client, client,
                        lb_service, port,
                        [services[1]],
                        "domain.abc.com", "/service1.html")

    validate_lb_service(admin_client, client,
                        lb_service, port,
                        [services[1]],
                        "domain.def.com", "/service1.html")

    validate_lb_service(admin_client, client,
                        lb_service, port,
                        [services[2]],
                        "abc.domain.com", "/name.html")

    validate_lb_service(admin_client, client,
                        lb_service, port,
                        [services[3]],
                        "abc.domain.com", "/service1.html")

    delete_all(client, [env])
