from django.db import models
from fluent_pages.models import UrlNode
from impact.models.mc_model import MCModel
from impact.models.program_role import ProgramRole


class NodePublishedFor(MCModel):
    node = models.ForeignKey(UrlNode)
    published_for = models.ForeignKey(ProgramRole)

    class Meta(MCModel.Meta):
        verbose_name = "Node is Published For"
        verbose_name_plural = "Node is Published For"

    def __str__(self):
        tmpl = "%s is available to %s"
        return tmpl % (self.node.title, self.published_for.name)
