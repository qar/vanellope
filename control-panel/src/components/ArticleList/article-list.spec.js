import { shallowMount } from '@vue/test-utils';
import apis from '@/utils/api';
import ArticleList from './article-list.vue';

describe('ArticleList component', () => {
  beforeEach(() => {
    apis.getArticleList = jest.fn().mockImplementation(() => Promise.resolve({
      data: [{
        title: 'example title',
        uuid: 'example-uuid',
        counts: '1',
      }],
      paging: {
        total: 10,
        items_per_page: 5,
      },
    }));

    shallowMount(ArticleList, {
      stubs: [
        'Page',
      ],
    });
  });

  it('An API should be called to fetch data when component initiated', () => {
    expect(apis.getArticleList).toHaveBeenCalledTimes(1);
  });
});
