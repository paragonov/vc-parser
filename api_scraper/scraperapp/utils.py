from celery.utils.log import get_task_logger

from .models import VcMV, VcCL, VcDNS

logger = get_task_logger(__name__)


def write_db(product_list, VcModel):
    new_count = 1
    if VcModel.objects.all():
        for product in product_list.values():
            vc = VcModel.objects.filter(id=new_count).update(
                name=product["product_name"],
                link=product["product_link"],
                price=product["product_price"],
                available=product["product_available"],
            )
            new_count += 1
    else:
        for product in product_list.values():
            vc = VcModel.objects.create(
                name=product["product_name"],
                link=product["product_link"],
                price=product["product_price"],
                available=product["product_available"],
            )
            vc.save()
            new_count += 1
    logger.info(f"New vc: {new_count} vc(s) added.")
    print(len(VcModel.objects.all()))


def save_db(product_list: dict, flag: str):
    if product_list:
        if flag == "Мвидео":
            VcModel = VcMV
            write_db(product_list, VcModel)
        elif flag == "DNS":
            VcModel = VcDNS
            write_db(product_list, VcModel)
        elif flag == "Citilink":
            VcModel = VcCL
            write_db(product_list, VcModel)
