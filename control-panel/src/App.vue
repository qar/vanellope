<template>
    <div class="layout">
        <Row type="flex">
            <Col span="4" class="layout-menu-left">
                <Menu active-name="1-2" theme="dark" width="auto" :open-names="['1']">
                    <div class="layout-logo-left"></div>
                    <Submenu name="1">
                        <template slot="title">
                            <Icon type="ios-navigate"></Icon>
                            文章
                        </template>
                        <MenuItem name="1-1">已发布</MenuItem>
                        <MenuItem name="1-2">草稿</MenuItem>
                        <MenuItem name="1-3">回收站</MenuItem>
                    </Submenu>
                </Menu>
            </Col>
            <Col span="20">
                <div class="layout-content">
                    <div class="layout-content-main">
                      <router-view></router-view>
                    </div>
                </div>
            </Col>
        </Row>
    </div>
</template>

<script>
export default {
};
</script>

