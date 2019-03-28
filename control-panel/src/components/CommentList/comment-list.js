/* eslint-disable */
import CommentsTable from './comments-table.vue';

export default {
  name: 'CommentList',
  components: {
    CommentsTable,
  },

  data () {
    return {
      // Active tab name
      activeState: 'checking',
    };
  },

  methods: {
    refresh() {
      switch (this.activeState) {
        case 'checking':
          this.$refs.checkingState.update();
          break;

        case 'approved':
          this.$refs.approvedState.update();
          break;

        case 'banned':
          this.$refs.bannedState.update();
          break;

        default:
          break;
      }
    },
  },
};
