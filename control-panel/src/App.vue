<template>
  <div>
    <div id="header" data-link="/">
      <a href="/">reader.page302.com</a>
    </div>

    <!-- nav zone -->
    <div id="navbar">
      <Menu active-name="1-2" theme="dark" width="auto" :open-names="['1']">
          <div class="layout-logo-left"></div>
          <Submenu name="1">
              <template slot="title">
                  <Icon type="ios-navigate"></Icon>
                  文章
              </template>
              <MenuItem name="1-1"><router-link to="/articles" tag="div">已发布</router-link></MenuItem>
              <MenuItem name="1-2">草稿</MenuItem>
              <MenuItem name="1-3">回收站</MenuItem>
          </Submenu>
      </Menu>
    </div>

    <!-- main content -->
    <div id="wrapper">
      <div id="wrapper-inner">
        <router-view></router-view>
      </div><!-- End of #wrapper-inner -->
    </div><!-- End of #wrapper -->
  </div>
</template>

<script>
export default {
};
</script>

<style scopped lang="scss">
  // in case of margin collapsing
  // https://www.w3.org/TR/CSS2/box.html#collapsing-margins
  .layout-logo-left {
    display: inline-block;
  }
</style>
