<template>
  <Tabs v-model="activeState" @on-click="refresh">

    <TabPane label="New" name="checking" icon="quote">
      <div class="article-list-layout">
        <h1 class="table-title">新评论</h1>
        <comments-table state="checking" ref="checkingState"></comments-table>
      </div>
    </TabPane>

    <TabPane label="Approved" name="approved" icon="heart">
      <div class="article-list-layout">
        <h1 class="table-title">审核通过的评论</h1>
        <comments-table state="approved" ref="approvedState"></comments-table>
      </div>
    </TabPane>

    <TabPane label="Banned" name="banned" icon="heart-broken">
      <div class="article-list-layout">
        <h1 class="table-title">被禁止的评论</h1>
        <comments-table state="banned" ref="bannedState"></comments-table>
      </div>
    </TabPane>
  </Tabs>
</template>

<script src="./comment-list.js"></script>

<style scoped lang="scss" src="./comment-list.scss"></style>
