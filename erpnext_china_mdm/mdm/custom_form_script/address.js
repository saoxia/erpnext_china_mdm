frappe.ui.form.on('Address', {
    state: function(frm) {
        // 当省字段发生变化时，获取省ID
        var state_id = frm.doc.state;

        if (state_id) {
            var filters = {
                'parent_territory': state_id
            };

            // 市字段应用过滤条件
            frm.set_query("city", function() {
                return {
                    filters: filters
                };
            });
        }
    }
});